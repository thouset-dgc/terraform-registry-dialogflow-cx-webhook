from utils.dialogflow_interface import make_response


def create_article(request: dict):

    
    parameters = {"param1": "value1", "param2": "value2"}
    return make_response(parameters=parameters)
