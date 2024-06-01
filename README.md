# podbook_rebound

Generate podcasts from audiobooks.

Based on the phenomenal [podbook by jpverkamp](https://github.com/jpverkamp/podbook), reworked for a modern hosting environment.

Expected directory structure:
- `./books/{author}/{book}/*.mp3`

The author's and book's title will be used for the podcast metadata.

mp3 files will be returned in order, using the filename as the chapter title.

Sets the publish time of each episode as a sequentially increment from the modified time of the first file in a book.

## Set-up

1. Set environment variables:
    * `UUID_NAMESPACE`: a random UUID of your choice.  This will be used generate deterministic hashes to put books behind in URLs.  Can generate using `uuidgen -r`.
    * `BOOKS_DIRECTORY`: filepath to the directory containing all the audiobook folders.
    * `BASIC_AUTH_USERNAME`: (optional) if you want basic auth, set to the username you want to use for basic auth.
    * `BASIC_AUTH_PASSWORD`: (optional) if you want basic auth, set to the password you want to use for basic auth.

## Running

```
docker run --rm -it \
  -p 8000:8000 \
  -v /path/to/your/audiobooks:/books \
  -e UUID_NAMESPACE=<a uuid> \
  dartagan/podbook-rebound`
```

## Development

### Simultaneous client/server development

1. Start the backend devserver using: `rye run devserver`
2. Start the frontend devserver using: `npm run dev`
3. In the browser, go to: `http://localhost:5000`

### Build docker container

`docker build --pull . -t podbook-rebound`


## TODO

* Clear use of the name podbook and its author, with its author - see license: https://github.com/jpverkamp/podbook/blob/master/LICENSE.md
* Figure out what's to be done with the LICENSE, convert to MIT?
* Server the files directly, cease using nginx.  Or maybe do keep using nginx... as gunicorn recommends.  More precisely, how to do either - depending on if we're running directly or via a container.  Probably have flask serve the files, but in the container provide a nginx configuration the supersedes it.  But we probably want the files to also be behind some form of auth/obfuscation... so maybe they're served by the application after all.
* Is `request.url.host` a good way to get the URL for making the feeds?
* async/await
* UUID alternative (same determinism + salting, maybe a more portable approach).  Maybe just hash of the title, plus an optional salt, also need to do something to prevent collisions... though I guess the filesystem would handle that.
* Bring back the masonry display for the authors/books
