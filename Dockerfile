FROM node:alpine as client-builder

RUN mkdir /app/
WORKDIR /app/

COPY client/package.json client/package-lock.json .
RUN npm install
COPY client .
RUN npm run build


FROM python:3-alpine

ENV PYTHONUNBUFFERED True
RUN mkdir /app/
WORKDIR /app/

COPY requirements.lock pyproject.toml README.md .

# TODO: try removing these extra dependencies/build-dependencies
RUN apk add --no-cache --virtual build-dependencies \
    musl-dev \
 && pip3 install -r requirements.lock \
 && apk del build-dependencies

COPY --from=client-builder /app/dist /app/client/dist
COPY server ./server

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "server.src.__main__:app"] }
