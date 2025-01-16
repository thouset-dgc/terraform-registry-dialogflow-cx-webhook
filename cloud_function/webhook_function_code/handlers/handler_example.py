from dataclasses import dataclass

from utils.base import HandlerBase
from utils.logger import get_logger

logger = get_logger(__name__.split('.')[-1])

@dataclass
class HandlerExample(HandlerBase):
    """Example handler for the 'handler_example' tag. This should be used as a template for creating new handlers."""
    def __call__(self, request):
        logger.info("Processing request with 'handler_example' handler.")
        return {
            "message_text": ["Hello, World!"],
            "parameters": {"foo": "bar"},
            "message_payload": [
                {
                    "text": {"text": ["Hello, World!"]}
                }
            ],
        }