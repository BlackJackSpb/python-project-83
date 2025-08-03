PORT ?= 8000

.PHONY: install dev build render-start start

install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run --host 0.0.0.0 --port $(PORT)

build:
	./build.sh

render-start:
	uv run python3 page_analyzer/models.py

start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
