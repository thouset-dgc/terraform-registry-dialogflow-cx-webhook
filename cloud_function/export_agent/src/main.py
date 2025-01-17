import os
from datetime import datetime
import functions_framework
from google.api_core.client_options import ClientOptions
from google.cloud.dialogflowcx_v3 import (
    AgentsClient,
    ExportAgentRequest,
)
from cloudevents.http import CloudEvent
import pytz
from logger import get_logger

logger = get_logger(__name__)

def export_agent(
    agent_id: str, bucket_name: str, file_name: str, environment: str, location: str
):
    """
    See documentation : https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents/export
    Exports the Dialogflow CX Agent with the Parameters provided:
    - agent_id - System generated unique name of the Agent of the format
    - projects/<project_id>/locations/<location>/agents/<Unique ID created for the agent>
    - bucket_name - Name of the Google Cloud Storage Bucket to export the agent to
    - file_name - Name of the file to export the agent to
    - environment - Environment to export the agent from
    """

    agents_client = AgentsClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-dialogflow.googleapis.com"
        )
    )

    request = ExportAgentRequest(
        name=agent_id,
        agent_uri=f"gs://{bucket_name}/{file_name}",
        environment=environment,
        # data_format=DataFormat.JSON_PACKAGE
    )
    logger.info(request)
    export_operation = agents_client.export_agent(request=request)
    logger.info("Exporting the Agent...")

    response = export_operation.result()

    return response


@functions_framework.cloud_event
def execute_export_agent(cloud_event: CloudEvent) -> None:
    """
    Executes the export of Dialogflow CX agent.

    Args:
        event: The event triggering the export (a Pub/Sub message).

    Returns:
        None
    """

    source_environment = cloud_event.data["message"]["attributes"]["source_environment"]

    time_zone = os.getenv("TIME_ZONE")
    blob_name = os.getenv("ARCHIVE_BLOB_NAME")
    location = os.getenv("DIALOGFLOW_LOCATION")
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
    agent_id = os.getenv("DIALOGFLOW_AGENT_ID")

    # date must be strftime("%Y-%m-%d-%H-%M") in the specified time zone
    date = datetime.now(pytz.timezone(time_zone)).strftime("%Y-%m-%d-%H-%M")

    if source_environment == "rec":
        landing_bucket_name = os.getenv("QA_LANDING_BUCKET_NAME")
        environment_id = os.getenv("DIALOGFLOW_QA_ENVIRONMENT_ID")
    elif source_environment == "hpr":
        landing_bucket_name = os.getenv("HPR_LANDING_BUCKET_NAME")
        environment_id = os.getenv("DIALOGFLOW_HPR_ENVIRONMENT_ID")
    elif source_environment == "prd":
        landing_bucket_name = os.getenv("PRD_LANDING_BUCKET_NAME")
        environment_id = os.getenv("DIALOGFLOW_PRD_ENVIRONMENT_ID")
    else:
        raise ValueError("Invalid source_environment")
    

    file_name = f"agent-{agent_id}-{date}-{source_environment}-{blob_name}"

    landing_bucket_name = f"{landing_bucket_name}"

    agent_export_response = export_agent(
        agent_id=f"projects/{project_id}/locations/{location}/agents/{agent_id}",
        bucket_name=landing_bucket_name,
        file_name=file_name,
        environment=f"projects/{project_id}/locations/{location}/agents/{agent_id}/environments/{environment_id}",
        location=location,
    )

    logger.info(
        f"Agent Exported\n{agent_export_response}"
    )


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    attributes = {
        "type": "com.example.sampletype1",
        "source": "https://example.com/event-producer",
    }
    data = {
        "message": {
            "data": "SGVsbG8sIFdvcmxkIQ==",
            "attributes": {"source_environment": "QA"},
        }
    }

    mock_cloud_event = CloudEvent(
        attributes=attributes,
        data=data,
    )

    execute_export_agent(mock_cloud_event)
