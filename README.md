# Dictionary transformer

AWS State language inspired library to convert dictionaries to different formats.

## Installation

```shell
pip install dictionary-transformer
```

## Example usage

```python
from dictionary_transformer import transform_json


data = {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe"
}

mapping = {
    "type": "user",
    "meta": {
        "firstName": "$.first_name",
        "lastName": "$.last_name"
    }
}

transform_json(data, mapping)

# Output
{
    "type": "user",
    "meta": {
        "firstName": "John",
        "lastName": "Doe"
    }
}
```

If input is of iterable type, the formatting will be applied to every single item in the list.

```python
from dictionary_transformer import transform_json


data = [
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe"
    },
    ...
]

mapping = {
    "type": "user",
    "meta": {
        "firstName": "$.first_name",
        "lastName": "$.last_name"
    }
}

transform_json(data, mapping)

# Output
[
    {
        "type": "user",
        "meta": {
            "firstName": "John",
            "lastName": "Doe"
        }
    },
    ...
]
```

You can also parse items from a list of objects into a list:

```python
from dictionary_transformer import transform_json


data = [
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe"
    },
    ...
]

mapping = {
    "type": "user_first_names",
    "firstNames": "$.[*].first_name"
}

transform_json(data, mapping)

# Output
{
    "type": "user_first_names",
    "firstNames": ["John"]
}
```
