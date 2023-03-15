import unittest

import dictionary_transformer.transformer
from dictionary_transformer import (
    TransformerException,
    is_value_a_mapping,
    transform_json,
)


class TestSomething(unittest.TestCase):
    def test_transformation(self):
        source = {
            "id": 1,
            "name": "Rimvydas",
            "position": {
                "role": "Software Engineer",
                "country": "Sweden",
                "detail": {"company": "RimCo"},
            },
        }

        mapping = {"type": "employee", "name": "$.name", "position": "$.position.role"}
        result = transform_json(source, mapping)
        expected = {
            "type": "employee",
            "name": "Rimvydas",
            "position": "Software Engineer",
        }

        self.assertEqual(expected, result)

    def test_list_transformation(self):
        source = [
            {
                "id": 1,
                "name": "Rimvydas",
                "position": {
                    "role": "Software Engineer",
                    "country": "Sweden",
                    "detail": {"company": "RimCo"},
                },
            },
            {
                "id": 2,
                "name": "John",
                "position": {
                    "role": "Product Manager",
                    "country": "Norway",
                    "detail": {"company": "RimCo"},
                },
            },
        ]

        mapping = {"type": "employee", "name": "$.name", "position": "$.position.role"}
        result = transform_json(source, mapping)
        expected = [
            {
                "type": "employee",
                "name": "Rimvydas",
                "position": "Software Engineer",
            },
            {
                "type": "employee",
                "name": "John",
                "position": "Product Manager",
            },
        ]

        self.assertEqual(expected, result)

    def test_retrieval_from_list(self):
        source = {
            "employees": [
                {
                    "id": 1,
                    "name": "Rimvydas",
                    "position": {
                        "role": "Software Engineer",
                        "country": "Sweden",
                        "detail": {"company": "RimCo"},
                    },
                },
                {
                    "id": 2,
                    "name": "John",
                    "position": {
                        "role": "Product Manager",
                        "country": "Norway",
                        "detail": {"company": "RimCo"},
                    },
                },
            ]
        }

        mapping = {
            "type": "employees",
            "names": "$.employees.[*].name",
            "positions": "$.employees.[*].position.role",
        }
        result = transform_json(source, mapping)
        expected = {
            "type": "employees",
            "names": [
                "Rimvydas",
                "John",
            ],
            "positions": [
                "Software Engineer",
                "Product Manager",
            ],
        }
        self.assertEqual(expected, result)

    def test_invalid_key(self):
        data = {"name": "Rim"}
        mapping = {"firstName": "$.first_name"}
        result = transform_json(data, mapping)
        expected = {
            "firstName": None,
        }
        dictionary_transformer.transformer.ignore_non_existent_keys = False
        self.assertEqual(expected, result)

        self.assertRaises(TransformerException, transform_json, data, mapping)

    def test_value_mappings(self):
        tests = (
            ("not.mapping", False),
            ("$.mapping.[*].name", True),
        )

        for test_string, result in tests:
            self.assertEqual(
                result,
                is_value_a_mapping(test_string),
                f"{test_string} should be {result}",
            )
