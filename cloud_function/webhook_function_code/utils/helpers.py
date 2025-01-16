from typing import Dict, List, Optional

from schemas.dialogflow import (ConditionalPayload, DialogflowResponse,
                                MessagePayload, TextMessage)


def get_tag(query: dict) -> str:
    """
    Extracts the tag from the Dialogflow CX webhook request.

    This function retrieves the tag from the 'fulfillmentInfo' field of the incoming Dialogflow CX webhook request.
    The tag is used to determine which specific action to perform based on the user's interaction with the chatbot.

    Args:
        query (dict): The Dialogflow CX webhook request as a dictionary.

    Returns:
        str: The extracted tag from the request.

    Raises:
        Exception: If the 'tag' is not found in the 'fulfillmentInfo' field of the request.
                   This indicates a misconfiguration in the Dialogflow CX webhook settings.
    """
    try:
        # Attempt to retrieve the 'tag' from the 'fulfillmentInfo' field of the request
        tag = query["fulfillmentInfo"]["tag"]

    except KeyError:
        raise ValueError(
            "No 'tag' found in fullfillmentInfo. Check Dialogflow CX webhook settings or input data."
        )
    # Return the extracted 'tag'
    return tag


def make_response(
    tag: str,
    parameters: Optional[Dict] = None,
    message_text: Optional[List[str]] = None,
    message_payload: Optional[List[Dict]] = None,
    message_conditional_payload: Optional[Dict] = None,
    status: str = "succeed",  # Defaults to "succeed" unless explicitly failed
) -> str:
    """
    Constructs a Dialogflow CX webhook response based on the provided parameters.

    This function constructs a Dialogflow CX webhook response using the provided parameters and fullfillment messages.
    A dynamic status key is added to the parameters to indicate the status of the response and will default to "succeed"
    unless explicitly failed. If any errors occur during the construction of the response, a default error response is 
    returned with the error message in order to provide a response to Dialogflow CX.

    Args:
        tag (str): The tag associated with the Dialogflow CX intent.
        parameters (Optional[Dict]): The parameters to include in the response.
        message_text (Optional[List[str]]): The text messages to include in the response.
        message_payload (Optional[List[Dict]]): The payload messages to include in the response.
        message_conditional_payload (Optional[Dict]): The conditional payload message to include in the response.
        status (str): The status of the response, defaults to "succeed".

    Returns:
        str: The JSON string representation of the Dialogflow CX webhook response.

    """

    dynamic_status_key = f"{tag}_status"
    try:
        parameters = parameters or {}
        parameters[dynamic_status_key] = status

        # Construct the response data
        response_data = {
            "sessionInfo": {"parameters": parameters},
            "fulfillmentResponse": (
                {"messages": []}
                if message_text or message_payload or message_conditional_payload
                else None
            ),
        }

        if message_text:
            response_data["fulfillmentResponse"]["messages"].extend(
                [
                    TextMessage(text=[text]).model_dump(mode="python")
                    for text in message_text
                ]
            )

        if message_payload:
            response_data["fulfillmentResponse"]["messages"].extend(
                [
                    MessagePayload(payload=payload).model_dump(mode="python")
                    for payload in message_payload
                ]
            )

        if message_conditional_payload:
            response_data["fulfillmentResponse"]["messages"].append(
                ConditionalPayload(**message_conditional_payload).model_dump(
                    mode="python"
                )
            )

        # Validate the final schema
        validated_response = DialogflowResponse(**response_data)

        # Return the JSON string
        return validated_response.model_dump(mode="json")

    except Exception as e:
        error_msg = f"Error building Dialogflow response: {str(e)}"
        
        return make_response(
            tag=tag,
            parameters={dynamic_status_key: "failed"},
            message_text=[error_msg],
            status="failed",
        )
