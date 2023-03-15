import unittest

from dictionary_transformer import transform_json


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
