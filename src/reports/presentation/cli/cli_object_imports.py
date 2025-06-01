import sys
from collections.abc import Generator
from contextlib import contextmanager
from importlib import import_module
from pathlib import Path
from typing import Any


@contextmanager
def add_cwd_in_path() -> Generator[None, None, None]:
    cwd = str(Path.cwd())
    if cwd not in sys.path:
        sys.path.insert(0, cwd)
        try:
            yield
        finally:
            sys.path.remove(cwd)
    else:
        yield


def import_object(object_spec: str) -> Any:
    module_name, object_name = object_spec.split(":", 1)
    if not object_name:
        raise ValueError(
            "Invalid object specification. Format should be '<module>:<object>'"
        )

    with add_cwd_in_path():
        module = import_module(module_name)
    return getattr(module, object_name)
