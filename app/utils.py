from typing import Iterable, Dict, Any


def error_list_to_str(data: Iterable[Any]) -> str:
    results = [error_data_to_str(item) for item in data]
    return ', '.join(results)


def error_dict_to_str(data: Dict[Any, Any]) -> str:
    results = [
        f'{error_data_to_str(k)}: {error_data_to_str(v)}'
        for k, v in data.items()
    ]
    return ', '.join(results)


def error_data_to_str(data: Any) -> str:
    if isinstance(data, str):
        result = data
    elif isinstance(data, dict):
        result = error_dict_to_str(data)
    elif isinstance(data, Iterable):
        result = error_list_to_str(data)
    else:
        result = str(data)
    return result
