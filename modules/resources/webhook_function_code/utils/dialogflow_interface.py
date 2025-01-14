import json


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
    except Exception as e:
        import logging 

        logging.exception(f"An unexpected error occured : {e}")
        raise
    # Return the extracted 'tag'
    return tag


def make_response(
    parameters: dict = None,
    message_text: list[str] = None,
    message_payload: list[dict] = None,
    message_conditional_payload: dict = None,
    error: dict = None
) -> str:
    """Builds a response for Dialogflow CX.

    Constructs a response with parameters, text messages, or payloads.  At least one
    of `parameters`, `message_text`, or `message_payload` must be provided.
        Args:
            parameters (dict, optional): Session parameters.
            message_text (list[str], optional): List of text messages.
            message_payload (list[dict], optional): List of payload messages.
            message_conditional_payload (dict, optional): Dictionary for conditional payloads.

        Returns:
            str: A JSON string representing the Dialogflow CX response.

        Raises:
            ValueError: If no parameters, message_text, or message_payload are provided.
            TypeError: If parameters, message_text, or message_payload have incorrect types.

    """
    if error :
        return json.dumps(error)

    if not any([parameters, message_text, message_payload]):
        return json.dumps(
            {
                "error": {
                    "code" : "",
                    "message": "At least one of 'parameters', 'message_text', or 'message_payload' must be provided."
                }
            }
        )
        raise ValueError(
            "At least one of 'parameters', 'message_text', or 'message_payload' must be provided."
        )

    if parameters is not None and not isinstance(parameters, dict):
        raise TypeError(f"Expected 'parameters' to be a dict, got {type(parameters)}")
    if message_text is not None and not isinstance(message_text, list):
        raise TypeError(
            f"Expected 'message_text' to be a list, got {type(message_text)}"
        )
    if message_payload is not None and not isinstance(message_payload, list):
        raise TypeError(
            f"Expected 'message_payload' to be a list, got {type(message_payload)}"
        )

    response = {}
    if parameters:
        response["sessionInfo"] = {"parameters": parameters}

    if message_text or message_payload:
        response["fulfillmentResponse"] = {"messages": []}
        if message_text:
            for text in message_text:
                response["fulfillmentResponse"]["messages"].append(
                    {"text": {"text": [text]}}
                )
        if message_payload:
            for payload in message_payload:
                response["fulfillmentResponse"]["messages"].append({"payload": payload})

    if message_conditional_payload:
        response["fulfillmentResponse"]["messages"].append(message_conditional_payload)

    return json.dumps(response)  # Return a JSON string
