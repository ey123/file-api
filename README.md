# File API

## Getting started

```
python app.py 
```

default PORT 7777 - configurable via env var PORT:

```
PORT=6666 python app.py
```
## Docker
In order to run the server via docker (PORT 6000)

```
docker build -t file-api .
docker run -p 6000:6000 --env PORT=6000 -v $(pwd)/public:/app/public file-api
```

## Documentation

API documentation is available at [http://127.0.0.1:7777/docs](http://127.0.0.1:7777/docs)

### Testing

Run tests with `make test`

### Linting

Run linting with `make lint`

### Formatting

Run formatting with `make format`