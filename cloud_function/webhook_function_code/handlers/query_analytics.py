# utils/handlers.py
from utils.bigquery import get_bigquery_sql_result
from utils.dialogflow_interface import make_response
import json 

def get_analytics_query(json_data):
    """
    Extracts the 'analytics_query' value from the JSON data.

    Args:
        json_data: A JSON string or a Python dictionary representing the JSON data.

    Returns:
        The value of 'analytics_query' as a string, or None if the key is not found.
    """
    try:
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else: 
            data = json_data

        return data["sessionInfo"]["parameters"]["analytics_query"]

    except (KeyError, TypeError):
        raise

def query_analytics(request: dict):
    query = get_analytics_query(request)

    query_result = get_bigquery_sql_result(sql_query=query)

    parameter_dict = {"query_result": query_result}
    
    return make_response(parameters=parameter_dict)
