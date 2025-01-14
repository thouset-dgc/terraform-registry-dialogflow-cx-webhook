# utils/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict

class HandlerBase(ABC):
    """Base class for all handlers."""

    @abstractmethod
    def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the incoming request."""
        pass
