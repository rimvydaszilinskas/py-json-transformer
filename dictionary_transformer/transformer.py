import re
from copy import deepcopy

skip_empty_iterations = False


class Undefined:
    ...


class Transformation:
    SPECIAL_SYMBOL_ALL = "[*]"
    SPECIAL_SYMBOL_SOURCE = "$"

    def __init__(self, key):
        self.__value = Undefined()
        self.__keys = list()
        self.__decompose_key(key)

    def __decompose_key(self, key):
        if not isinstance(key, str):
            self.__value = key
            return
        values = key.split(".")
        if values[0] != self.SPECIAL_SYMBOL_SOURCE:
            self.__value = key
            return
        self.__keys = values[1:]

    @staticmethod
    def __is_key_index(key):
        expression = r"\[(\d+)\]"
        results = re.search(expression, key)
        if results:
            return int(results.groups()[0])

    @staticmethod
    def __get_keys_from_iterable(key, iterable):
        def get(k, obj):
            try:
                return obj[k]
            except (KeyError, TypeError):
                if skip_empty_iterations:
                    return None

        return list(get(key, i) for i in iterable)

    @classmethod
    def __get_value_by_key(cls, key: str, value):
        idx = cls.__is_key_index(key)
        if idx is not None:
            return value[idx]
        if key == cls.SPECIAL_SYMBOL_ALL:
            return value
        if isinstance(value, (list, tuple, set)):
            return cls.__get_keys_from_iterable(key, value)
        return value[key]

    def get_value(self, source: dict):
        if not isinstance(self.__value, Undefined):
            return self.__value

        if len(self.__keys) == 0:
            return source

        return_value = deepcopy(source)
        for key in self.__keys:
            return_value = self.__get_value_by_key(key, return_value)
        return return_value

    def __call__(self, source: dict):
        return self.get_value(source)


def is_value_a_mapping(value):
    pattern = r"(\$((.?)([a-z]+|\[\*\]|\[\d+\]))+)"
    return re.search(pattern, value) is not None


def transform_key(key, source):
    if isinstance(key, (list, set, tuple)):
        return list(Transformation(k)(source) for k in key)
    return Transformation(key)(source)


def transform_json(source, mapping: dict):
    if isinstance(source, (list, tuple, set)):
        return [transform_json(item, mapping) for item in source]

    def get_value(value):
        if isinstance(value, dict):
            return transform_json(source, value)
        return transform_key(value, source)

    return {key: get_value(value) for key, value in mapping.items()}
