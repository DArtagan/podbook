# podbook_rebound

Generate podcasts from audiobooks.

Based on the phenomenal [podbook by jpverkamp](https://github.com/jpverkamp/podbook), reworked for a modern hosting environment.

Expected directory structure:
- `./books/{author}/{book}/*.mp3`

The author's and book's title will be used for the podcast metadata.

mp3 files will be returned in order, using the filename as the chapter title.

Sets the publish time of each episode as a sequentially increment from the modified time of the first file in a book.

## Set-up

1. Docker container or python
2. Set environment variables:
    * `UUID_NAMESPACE`: a random UUID of your choice.  This will be used generate deterministic hashes to put books behind in URLs.
    * `BOOKS_DIRECTORY`: filepath to the directory containing all the audiobook folders.


## Development

* `rye run devserver`
* `rye run server`
* `npm run dev`
* `npm run build`
* `docker build`


## TODO

* Clear use of the name podbook and its author, with its author - see license: https://github.com/jpverkamp/podbook/blob/master/LICENSE.md
* Figure out what's to be done with the LICENSE, convert to MIT?
* Server the files directly, cease using nginx.  Or maybe do keep using nginx... as gunicorn recommends.  More precisely, how to do either - depending on if we're running directly or via a container.  Probably have flask serve the files, but in the container provide a nginx configuration the supersedes it.  But we probably want the files to also be behind some form of auth/obfuscation... so maybe they're served by the application after all.
* Do something to get rid of URL_SCHEME
* UUID alternative (same determinism + salting, maybe a more portable approach)
* Svelte front-end?  And typescript?
* FastAPI back-end?  Or at least starlette?
