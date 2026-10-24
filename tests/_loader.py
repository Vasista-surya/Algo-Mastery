"""Import standalone examples without renaming the original folders or files."""

from functools import lru_cache
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


@lru_cache(maxsize=None)
def load(relative_path):
    path = (ROOT / relative_path).resolve()
    path.relative_to(ROOT)
    name = "algo_" + "_".join(path.relative_to(ROOT).with_suffix("").parts)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    # Dataclasses and other introspection tools need the module registered.
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module
