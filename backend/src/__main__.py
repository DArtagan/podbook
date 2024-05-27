import collections
import datetime
import functools
import glob
import os
import pathlib
import uuid

import feedgen.feed
import flask
import tinytag


UUID_NAMESPACE = uuid.UUID(os.environ.get("UUID_NAMESPACE", str(uuid.uuid4())))
BOOKS_DIRECTORY = os.environ.get("BOOKS_DIRECTORY", "/books")
FORMATS = ["mp3", "m4b"]
CLIENT_DIST_DIR = (pathlib.Path(__file__) / "../../../frontend/dist").resolve()

app = flask.Flask(__name__, static_folder=CLIENT_DIST_DIR / "static")


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

            if not any(file.endswith(tuple(FORMATS)) for file in os.listdir(book_path)):
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


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def catch_all(path):
    return flask.send_from_directory(CLIENT_DIST_DIR, path)


@app.route("/api/books-by-author")
def api_books_by_author():
    library = books_and_uuid_by_author()
    return flask.jsonify(
        [
            {
                "author": author,
                "books": [
                    {"title": book[0], "uuid": book[1]} for book in library[author]
                ],
            }
            for author in library
        ]
    )


@app.route("/feed/<uuid>.xml")
def get_feed(uuid):
    author, title = uuid_to_book(uuid)

    fg = feedgen.feed.FeedGenerator()
    fg.load_extension("podcast")

    host_url = (flask.request.scheme) + "://" + flask.request.host
    feed_link = host_url + "/feed/{uuid}.xml".format(uuid=uuid)

    fg.id = feed_link
    fg.title(title)
    fg.description("{title} by {author}".format(title=title, author=author))
    fg.author(name=author)
    fg.link(href=feed_link, rel="alternate")

    images = [
        os.path.basename(i)
        for i in glob.glob(os.path.join(BOOKS_DIRECTORY, author, title, "cover*"))
    ]
    if images:
        url = host_url + "/media/{author}/{title}/{image}".format(
            author=author, title=title, image=images[0]
        )
        fg.image(url)
        fg.podcast.itunes_image(url)

    fg.podcast.itunes_category("Arts")

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

        feed_entry_link = host_url + "/media/{author}/{title}/{file}".format(
            author=author, title=title, file=file
        )
        feed_entry_link = feed_entry_link.replace(" ", "%20")

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

    return fg.rss_str(pretty=True)


@app.route("/media/<path:path>")
def get_file(path):
    return flask.send_from_directory(BOOKS_DIRECTORY, path.replace("%20", " "))
