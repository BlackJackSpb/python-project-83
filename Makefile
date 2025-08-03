PORT ?= 8000

install:
    uv sync

dev:
    uv run flask --debug --app page_analyzer:app run

build:
    ./build.sh

start:
    uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

migrate:
    uv run python init_db.py

render-start:
    uv run python init_db.py && gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
