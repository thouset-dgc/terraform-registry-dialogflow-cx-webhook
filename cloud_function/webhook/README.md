# Dialogflow CX Webhook

This webhook handles incoming requests from Dialogflow CX, routing them to the appropriate handler based on the provided `tag`.

## Setup

1. **Deploy:** Deploy this code to a serverless platform like Cloud Functions.
2. **Configure Webhook:** In your Dialogflow CX agent, configure a webhook that points to the deployed function's URL.

## Request Format

The webhook expects a JSON payload in the following format:

```json
{
  "fulfillmentInfo": {
    "tag": "your_tag"
  },
  "sessionInfo": {
    "parameters": {
      "param1": "value1",
      "param2": "value2"
    }
  }
}
```
- `tag`: A string identifying the specific handler to invoke. This tag must match a key in the TAG_HANDLERS dictionary within the webhook code.
- `parameters`: An object containing parameters extracted by Dialogflow CX, accessible within the handler functions.

## Response Format
The webhook returns a JSON response. A successful response will have a 200 status code and look like this:

```json
{
  "fulfillment_response": {
    "messages": [
      {
        "text": {
          "text": ["Your success message here."]
        }
      }
    ]
  }
}
```
An error response will have a 400 or 500 status code and include an `error` message:

```json
{
  "error": "Error message here"
}
```

## Code Overview
The main function `webhook_entrypoint` receives the request, extracts the tag, and calls the corresponding handler function from the `TAG_HANDLERS` dictionary. Error handling and logging are implemented to ensure robustness.

## Example Handler (using make_response)
```python
from flask import make_response, jsonify

def your_tag_handler(request):
    # Access parameters (if needed)
    # parameters = request.get_json().get("sessionInfo", {}).get("parameters", {})

    # Construct successful response using make_response
    response = make_response(jsonify({
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": ["Success! This uses make_response."]
                    }
                }
            ]
        }
    }))
    response.status_code = 200  # Explicitly set 200 status code
    return response

# ... (rest of the webhook code)

TAG_HANDLERS = {
    "your_tag": your_tag_handler,
    // ... other handlers
}
```
This example demonstrates how to use `make_response` to create a successful response. The make_response function creates a Dialogflow-compatible `response` (json) object which gives you full control over status code, headers and response body.

## Error Handling
The webhook includes comprehensive error handling for missing tags, unknown tags, and exceptions within the handler functions, returning appropriate error messages and status codes. Detailed logging helps in debugging.

## Webhook Factory
```
webhook_function_code/
├── handlers/
│   ├── __init__.py
│   ├── handler_a.py
│   ├── handler_b.py
├── services/
│   ├── __init__.py
├── utils/
│   ├── __init__.py
│   ├── base.py    # Définit HandlerBase
│   ├── factory.py # Définit HandlerFactory
│   ├── dialogflow_interface.py
├── main.py
├── README.md
├── requirements.txt
```