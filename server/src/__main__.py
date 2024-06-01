import collections
import datetime
import functools
import glob
import os
import pathlib
from urllib import parse
import uuid
import secrets

import feedgen.feed
import fastapi
from fastapi import security, staticfiles
import tinytag

BASIC_AUTH_USERNAME = os.environ.get("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD = os.environ.get("BASIC_AUTH_PASSWORD")
BOOKS_DIRECTORY = os.environ.get("BOOKS_DIRECTORY", "/books")
CLIENT_DIST_DIR = (pathlib.Path(__file__) / "../../../client/dist").resolve()
FORMATS = ["mp3", "m4b"]
UUID_NAMESPACE = uuid.UUID(os.environ.get("UUID_NAMESPACE", str(uuid.uuid4())))

basic_auth = security.HTTPBasic()


async def verify_basicauth(request: fastapi.Request):
    if not BASIC_AUTH_USERNAME and not BASIC_AUTH_PASSWORD:
        return
    credentials = await basic_auth(request)
    if credentials:
        correct_username = secrets.compare_digest(
            credentials.username, BASIC_AUTH_USERNAME
        )  # type: ignore
        correct_password = secrets.compare_digest(
            credentials.password, BASIC_AUTH_PASSWORD
        )  # type: ignore
        if correct_username and correct_password:
            return
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


app = fastapi.FastAPI()
api = fastapi.FastAPI(
    title="API: podbook_reloaded", dependencies=[fastapi.Depends(verify_basicauth)]
)

app.mount("/api", api)
app.mount(
    "/media", name="media", app=staticfiles.StaticFiles(directory=BOOKS_DIRECTORY)
)


def list_books():
    """List all known books as (author, title) tuples."""
    for author in os.listdir(BOOKS_DIRECTORY):
        author_path = os.path.join(BOOKS_DIRECTORY, author)
        if not os.path.isdir(author_path):
            continue

        for title in os.listdir(author_path):
            book_path = os.path.join(author_path, title)
            if not os.path.isdir(book_path):
                continue

            yield (author, title)


def book_to_uuid(author, title):
    """Translate a book folder into a deterministic UUID."""
    return uuid.uuid5(UUID_NAMESPACE, author + title)


def uuid_to_book(id, cache={}):
    """Translate a UUID from above back into a book folder."""
    if not isinstance(id, uuid.UUID):
        id = uuid.UUID(id)

    if id not in cache:
        cache.clear()
        for author, title in list_books():
            cache[book_to_uuid(author, title)] = (author, title)

    if id not in cache:
        raise Exception("{} does not match any known book".format(id))

    return cache[id]


@functools.cache
def books_and_uuid_by_author():
    library = collections.defaultdict(list)
    for author, title in list_books():
        book = (title, book_to_uuid(author, title))
        library[author].append(book)
    return library


@api.get("/books-by-author")
def api_books_by_author():
    library = books_and_uuid_by_author()
    return [
        {
            "author": author,
            "books": [{"title": book[0], "uuid": book[1]} for book in library[author]],
        }
        for author in library
    ]


@app.get("/feed/{uuid}.xml")
async def get_feed(uuid: uuid.UUID, request: fastapi.Request):
    author, title = uuid_to_book(uuid)

    fg = feedgen.feed.FeedGenerator()
    fg.load_extension("podcast")

    feed_link = str(request.url_for("get_feed", uuid=uuid))

    fg.id = feed_link
    fg.title(title)
    fg.description("{title} by {author}".format(title=title, author=author))
    fg.author(name=author)
    fg.link(href=feed_link, rel="self")

    images = [
        os.path.basename(i)
        for i in glob.glob(os.path.join(BOOKS_DIRECTORY, author, title, "cover*"))
    ]
    if images:
        image_filepath = f"/{author}/{title}/{images[0]}"
        image_url = str(request.url_for("media", path=parse.quote(image_filepath)))
        fg.image(image_url)
        fg.podcast.itunes_image(image_url)

    base_path = os.path.join(BOOKS_DIRECTORY, author, title)

    def get_tracknumber_from_file(filepath):
        try:
            return int(tinytag.TinyTag.get(os.path.join(base_path, filepath)).track)
        except tinytag.TinyTagException:
            return 0

    files = glob.glob(os.path.join(base_path, "*"))
    files = sorted(files, key=get_tracknumber_from_file)
    files = [os.path.basename(i) for i in files]
    initial_time = datetime.datetime.utcfromtimestamp(
        os.path.getmtime(os.path.join(BOOKS_DIRECTORY, author, title, files[0]))
    )

    for index, file in enumerate(files):
        if not file.endswith(tuple(FORMATS)):
            continue

        filepath = f"/{author}/{title}/{file}"
        feed_entry_link = str(request.url_for("media", path=parse.quote(filepath)))

        fe = fg.add_entry()

        try:
            track = tinytag.TinyTag.get(os.path.join(base_path, file))
            name = track.title
        except tinytag.TinyTagException:
            name = file.rsplit(".", 1)[0]

        fe.id(feed_entry_link)
        fe.title(name)
        fe.description(
            "{title} by {author} - {chapter}".format(
                title=title,
                author=author,
                chapter=name,
            )
        )
        fe.pubDate(
            "{} +0000".format(initial_time + datetime.timedelta(seconds=90 * index))
        )
        fe.enclosure(feed_entry_link, 0, "audio/mpeg")

    return fastapi.Response(
        content=fg.rss_str(pretty=True), media_type="application/rss+xml"
    )


class AuthStaticFiles(staticfiles.StaticFiles):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send) -> None:
        assert scope["type"] == "http"
        request = fastapi.Request(scope, receive)
        await verify_basicauth(request)
        await super().__call__(scope, receive, send)


# Last, to redirect all remaining calls to the static files
app.mount("/", AuthStaticFiles(directory=CLIENT_DIST_DIR, html=True))
