from dataclasses import dataclass
from utils.base import HandlerBase


@dataclass
class HandlerExample(HandlerBase):
    """Example handler for the 'example' tag. This should be used as a template for creating new handlers."""
    def __call__(self, request):
        return {
            "message_text": ["Hello, World!"],
            "parameters": {"foo": "bar"},
            "message_payload": [
                {
                    "text": {"text": ["Hello, World!"]}
                }
            ],
        }