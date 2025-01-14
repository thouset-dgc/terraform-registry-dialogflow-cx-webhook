import logging

from flask import Request, jsonify
from handlers.query_analytics import query_analytics
from handlers.create_article import create_article
from utils.dialogflow_interface import get_tag


TAG_HANDLERS = {
    "query_analytics": query_analytics,
    "create_article": create_article,
}


def webhook_entrypoint(request: Request):
    """Entry point for the Dialogflow CX webhook.

    This function handles incoming webhook requests from Dialogflow CX, routing them to the appropriate handler function based on the 'tag' provided in the request.  It also includes robust error handling and logging.

    Args:
        request (flask.Request): The incoming webhook request from Dialogflow CX.  It should contain a JSON payload with a 'fulfillmentInfo' section that includes the 'tag' to identify the appropriate handler. Example:
        ```json
        {
          "fulfillmentInfo": {
            "tag": "tag_1"
          },
          "sessionInfo": {
            "parameters": {
              "param1": "value1"
            }
          }
        }
        ```

    Returns:
        flask.Response: A JSON response containing the result of the handler function, or an error message if the tag is unknown or an exception occurs. A tuple containing the response and HTTP status code.  The status code will be 200 on success, 400 for invalid requests (e.g., missing tag), and 500 for internal server errors.
           Example Success:
           ```json
           {
             "message": "Successful response" (ie. make_response(...) result)
           }
           ```
           Example Error:
           ```json
           {
             "error": "Unknown tag: invalid_tag"
           }
           ```

    Raises:
        ValueError: If the 'tag' is missing or invalid in the Dialogflow CX webhook request.
        Exception: For any other unexpected errors during request processing or within the handler functions.
    """

    try:
        query_json = request.get_json()
        tag = get_tag(query_json)
        logging.info(f"Processing tag: {tag}")

        handler = TAG_HANDLERS.get(tag)

        if handler:
            try:
                return handler(request=query_json)
            except Exception as e:
                # TODO : Handle errors in make_response body
                logging.exception(f"Error in handler for tag '{tag}': {e}")
                return jsonify(
                    {"error": f"An error occurred during processing for tag {tag}"}
                ), 500
        else:
            return jsonify({"error": f"Unknown tag: {tag}"}), 400

    except ValueError as e:
        # TODO : Handle errors in make_response body
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # TODO : Handle errors in make_response body
        logging.exception(f"An unexpected error occurred in webhook: {e} for tag {tag}")
        return jsonify({"error": f"An unexpected error occurred for tag {tag}."}), 500
