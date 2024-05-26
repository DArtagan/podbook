FROM python:3-alpine

RUN mkdir /app/
WORKDIR /app/

ADD requirements.lock pyproject.toml README.md .

# TODO: try removing these extra dependencies/build-dependencies
RUN apk add --no-cache \
    libxslt \
 && apk add --no-cache --virtual build-dependencies \
    gcc \
    libxml2-dev \
    libxslt-dev \
    musl-dev \
 && pip3 install -r requirements.lock \
 && apk del build-dependencies

ENV PYTHONUNBUFFERED True

ADD . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.src.back.__main__:app"]
