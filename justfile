set shell := ['bash', '-c']

help:
    just -l

install:
    uv sync --all-extras --all-groups

tests: install
    just _cargo --bin run_tests

run-app:
    just _cargo --bin run_app

stop-app:
    just _cargo --bin stop_app

_py *args:
    uv run {{args}}

_cargo *args:
    cargo run {{args}}
