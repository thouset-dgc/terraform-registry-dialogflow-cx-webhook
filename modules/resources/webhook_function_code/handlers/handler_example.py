from dataclasses import dataclass
from utils.base import HandlerBase


@dataclass
class HandlerExample(HandlerBase):
    """Handler for tag 'example'."""
    def __call__(self, request):
        return {"message": "Handler \"example\" called", "data": request}