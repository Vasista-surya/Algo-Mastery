"""Keep the documented category/algorithm/language layout complete."""

import contextlib
import importlib.util
import io
import re
import sys
import unittest
from unittest.mock import patch
from urllib.parse import unquote

from _loader import ROOT, load

CHECKS = load("tools/check_examples.py")


class RepositoryTests(unittest.TestCase):
    def test_each_category_has_documentation_and_complete_language_triplets(self):
        for category in CHECKS.CATEGORIES:
            directory = ROOT / category
            with self.subTest(category=category):
                self.assertTrue((directory / "README.md").is_file())
                algorithms = [path for path in directory.iterdir() if path.is_dir()
                              and not path.name.startswith((".", "__"))]
                self.assertTrue(algorithms)
                for algorithm in algorithms:
                    for suffix in (".py", ".java", ".c"):
                        sources = list(algorithm.glob("*" + suffix))
                        self.assertEqual(len(sources), 1, str(algorithm))
                        expected = algorithm.name.replace(" ", "")
                        if algorithm.name == "BubbleSort" and suffix == ".py":
                            expected = "Bubble-Sort"
                        self.assertEqual(sources[0].stem, expected)

    def test_python_imports_have_no_interactive_or_output_side_effects(self):
        for category in CHECKS.CATEGORIES:
            for path in (ROOT / category).glob("*/*.py"):
                with self.subTest(path=path.relative_to(ROOT)):
                    name = "import_check_" + path.stem
                    spec = importlib.util.spec_from_file_location(name, path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[name] = module
                    output = io.StringIO()
                    try:
                        with patch("builtins.input", side_effect=AssertionError("input during import")):
                            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                                spec.loader.exec_module(module)
                        self.assertEqual(output.getvalue(), "")
                    finally:
                        sys.modules.pop(name, None)

    def test_readme_relative_links_exist(self):
        for readme in (ROOT / "README.md", *(ROOT / name / "README.md" for name in CHECKS.CATEGORIES)):
            with self.subTest(readme=readme.relative_to(ROOT)):
                text = readme.read_text(encoding="utf-8")
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                    if target.startswith(("#", "https://", "http://", "mailto:")):
                        continue
                    target = unquote(target.split("#", 1)[0])
                    self.assertTrue((readme.parent / target).exists(), f"Broken link: {target}")


if __name__ == "__main__":
    unittest.main()
