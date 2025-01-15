from flask import Request
from utils.factory import HandlerFactory
from utils.helpers import get_tag, make_response

import logging

factory = HandlerFactory()


def webhook_entrypoint(request: Request):
    """
    Entry point for the webhook function. This function is the entry point of the Cloud Run Function that handles
    incoming requests from Dialogflow CX. It extracts the tag from the request, retrieves the appropriate handler
    based on the tag, and processes the request using the handler. The response is then constructed and returned
    to Dialogflow CX.

    Args:
        request (Request): The incoming request from Dialogflow CX.

    Returns:
        str: The response to be sent back to Dialogflow CX.

    """
    try:
        request_data = request.get_json()
        tag = get_tag(request_data)
        handler = factory(tag)

        response_data = handler(request_data)

        # Build response with dynamic status (succeed)
        return make_response(tag=tag, **response_data)

    except Exception as e:
        error_type = type(e).__name__
        logging.error(f"{error_type}: {e}")

        # Build response with dynamic status (failed)
        error_parameters = {"error_log": f"{error_type}: {e}"}
        return make_response(tag=tag, parameters=error_parameters, status="failed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting webhook server.")

    data = {"fulfillmentInfo": {"tag": "example"}}

    request = Request.from_values(json=data)

    response = webhook_entrypoint(request)

    logging.info(response)
