# podbook
Generate podcasts from audiobooks

Expected directory structure:
- `./books/{author}/{book}/*.mp3`

The author's and book's title will be used for the podcast metadata.

mp3 files will be returned in order, using the filename as the chapter title.

It is assumed that you've otherwise configured nginx to serve your static files.  A configuration file has been provided.

Sets the publish time of each episode as a sequentially increment from the modified time of the first file in a book.
