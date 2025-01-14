from flask import Request
from utils.factory import HandlerFactory
from utils.helpers import get_tag

import logging

factory = HandlerFactory()

def webhook_entrypoint(request: Request):
    """Main webhook entrypoint."""
    try:
        request_data = request.get_json()
        tag = get_tag(request_data)

        handler = factory(tag)

        response = handler(request_data)
        return response
    except ValueError as e:
        return e
    except Exception as e:
        return e

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting webhook server.")

    data = {
        "fulfillmentInfo": {
            "tag": "example"
        }
    }

    request = Request.from_values(json=data)

    response = webhook_entrypoint(request)

    logging.info(response)
