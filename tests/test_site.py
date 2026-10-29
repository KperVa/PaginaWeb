"""Pruebas de integración estática para la página, ejecutables con unittest."""

import re
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]


class SiteHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = Counter()
        self.ids = []
        self.classes = set()
        self.links = []
        self.local_resources = []
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.tags[tag] += 1

        element_id = attributes.get("id")
        if element_id:
            self.ids.append(element_id)

        self.classes.update(attributes.get("class", "").split())

        href = attributes.get("href", "")
        if tag == "a" and href.startswith("#"):
            self.links.append(href[1:])
        elif tag == "link" and "stylesheet" in attributes.get("rel", "").split():
            self.add_local_resource(href)

        if tag == "img":
            self.add_local_resource(attributes.get("src", ""))
        elif tag == "script":
            self.scripts.append(attributes)

    def add_local_resource(self, resource):
        parsed_resource = urlsplit(resource)
        if resource and not parsed_resource.scheme and not parsed_resource.netloc:
            self.local_resources.append(resource)


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "styles.css").read_text(encoding="utf-8")
        cls.javascript = (ROOT / "script.js").read_text(encoding="utf-8")
        cls.parser = SiteHTMLParser()
        cls.parser.feed(cls.html)
        cls.parser.close()

    def test_document_uses_spanish_and_semantic_landmarks(self):
        self.assertRegex(self.html, r"<html\b[^>]*\blang=[\"']es[\"']")
        for landmark in ("header", "nav", "main", "footer"):
            with self.subTest(landmark=landmark):
                self.assertGreater(self.parser.tags[landmark], 0)

    def test_ids_are_unique_and_internal_links_resolve(self):
        duplicates = [
            element_id
            for element_id, count in Counter(self.parser.ids).items()
            if count > 1
        ]
        self.assertEqual(duplicates, [], "Los identificadores HTML deben ser únicos.")

        available_ids = set(self.parser.ids)
        missing_targets = sorted(
            {target for target in self.parser.links if target not in available_ids}
        )
        self.assertEqual(
            missing_targets,
            [],
            "Todos los enlaces internos deben apuntar a un elemento existente.",
        )

    def test_local_stylesheet_and_images_exist(self):
        for resource in self.parser.local_resources:
            with self.subTest(resource=resource):
                self.assertTrue(resource, "El recurso local debe tener una ruta.")
                self.assertTrue(
                    (ROOT / resource).is_file(),
                    f"No se encontró el recurso local: {resource}",
                )

    def test_deferred_script_and_its_dom_selectors_are_wired(self):
        local_scripts = [
            script
            for script in self.parser.scripts
            if script.get("src") == "script.js"
        ]
        self.assertEqual(len(local_scripts), 1)
        self.assertIn("defer", local_scripts[0])

        selectors = re.findall(
            r"""querySelector(?:All)?\(\s*["']([.#][\w-]+)["']""",
            self.javascript,
        )
        self.assertTrue(selectors, "Se esperaban selectores DOM en script.js.")
        for selector in selectors:
            with self.subTest(selector=selector):
                if selector.startswith("#"):
                    self.assertIn(selector[1:], self.parser.ids)
                else:
                    self.assertIn(selector[1:], self.parser.classes)

    def test_stylesheet_supports_responsive_and_reduced_motion(self):
        self.assertRegex(self.css, r"@media\s*\(max-width:\s*\d+px\)")
        self.assertIn("@media (prefers-reduced-motion: reduce)", self.css)


if __name__ == "__main__":
    unittest.main()
