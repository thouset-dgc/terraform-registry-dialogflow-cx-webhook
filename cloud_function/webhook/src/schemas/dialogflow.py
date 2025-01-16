# schemas/dialogflow.py
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class ConditionalPayload(BaseModel):
    """Schema for conditional payload."""
    condition: str
    content: Dict


class TextMessage(BaseModel):
    """Schema for a text message."""
    text: List[str]


class MessagePayload(BaseModel):
    """Schema for a payload message."""
    payload: Dict


class DialogflowResponse(BaseModel):
    """Schema for the Dialogflow CX webhook response."""
    sessionInfo: Optional[Dict[str, Any]] = None
    fulfillmentResponse: Optional[Dict[str, List[Union[TextMessage, MessagePayload, ConditionalPayload]]]] = None
