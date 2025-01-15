from typing import Dict, Type

from handlers import HandlerExample
from utils.base import HandlerBase


class HandlerFactory:
    """Factory for creating handlers based on a tag."""
    _handlers: Dict[str, Type[HandlerBase]] = {
        "example": HandlerExample,
    }

    def __call__(self, tag: str):
        handler_class = self._handlers.get(tag)
        if not handler_class:
            raise ValueError(f"Unknown handler tag: {tag}")
        return handler_class()
