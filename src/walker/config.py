import functools
import operator as op
from typing import Any, Mapping, Type

_NoDefault = object()


def get(config: dict[str, Any], *keys: str, cls: Type = None, default: Any = _NoDefault) -> Any:
    """Retrieves the value of a configuration item."""
    try:
        value = functools.reduce(op.getitem, keys, config)
    except KeyError:
        if default is not _NoDefault:
            return default
        raise KeyError(f"Unknown config key '{'_'.join(keys)}'")

    if cls is not None:
        try:
            value = cls(value)
        except ValueError:
            raise ValueError(f"Invalid value {value} for type '{cls.__name__}'")

    return value


def has(config: dict[str, Any], *keys: str) -> bool:
    """Checks whether a configuration has an item."""
    try:
        functools.reduce(op.getitem, keys, config)
    except KeyError:
        return False
    else:
        return True


def update(config: dict[str, Any], source: Mapping[str, Any]) -> dict[str, Any]:
    """Deeply updates a configuration.

    Update is performed in-place.
    """
    for key, source_value in source.items():
        if key in config and isinstance(config[key], dict) and isinstance(source_value, dict):
            config[key] = update(config[key], source_value)
        else:
            config[key] = source_value

    return config


__all__ = ["get", "has", "update"]
