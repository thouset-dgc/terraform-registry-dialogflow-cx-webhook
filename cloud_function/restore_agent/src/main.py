import os

from cloudevents.http import CloudEvent
import functions_framework

from dfcx_scrapi.core.webhooks import Webhooks

from google.cloud.dialogflowcx_v3beta1 import types
from google.cloud.dialogflowcx_v3 import (
    AgentsClient,
    RestoreAgentRequest,
)
from google.api_core.client_options import ClientOptions

from google.cloud import storage

from logger import get_logger

logger = get_logger(__name__)


def move_file(source_bucket_name: str, destination_bucket_name: str, blob_path: str):
    """
    Move a file a to new subfolder as root.

    Args:
        source_bucket_name (str): The name of the source bucket.
        destination_bucket_name (str): The name of the destination bucket.
        blob_path (str): The path to the file to move.
    """
    logger.info(f"Moving {blob_path} from {source_bucket_name} to {destination_bucket_name}")
    # connect to the Cloud Storage client
    storage_client = storage.Client()

    # get the source bucket
    source_bucket = storage_client.get_bucket(source_bucket_name)

    # get the blob
    blob = source_bucket.blob(blob_path)

    # get the destination bucket
    destination_bucket = storage_client.get_bucket(destination_bucket_name)

    # copy the blob to the destination bucket
    new_blob = source_bucket.copy_blob(blob, destination_bucket)

    # delete the original blob
    blob.delete()

    logger.info(f"Moved {blob_path} to {destination_bucket_name}")


def restore_agent(agent_id: str, bucket_name: str, file_name: str, location: str):
    """
    See documentation : https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents/restore
    Restores the Dialogflow CX Agent with the Parameters provided:
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

    request = RestoreAgentRequest(
        name=agent_id,
        agent_uri=f"gs://{bucket_name}/{file_name}",
    )

    logger.info(request)

    restore_operation = agents_client.restore_agent(request=request)
    logger.info("Restoring the Agent...")
    response = restore_operation.result()

    logger.info(f"The Agent has successfully been restored to {agent_id}")
    return response


def check_id_token(agent_id: str):
    """
    Checks if the service agent authentication is set to ID_TOKEN for each Webhook in the provided Agent.

    Args:
        agent_id (str): The name of the agent.
    """
    w = Webhooks()

    webhooks_list = w.list_webhooks(agent_id=agent_id)

    for webhook in webhooks_list:
        my_service = types.Webhook.GenericWebService(
            service_agent_auth="ID_TOKEN", uri=webhook.generic_web_service.uri
        )

        # Update Webhook
        updated_webhook = w.update_webhook(webhook.name, generic_web_service=my_service)

        logger.info(f"{updated_webhook.display_name} updated to ID_TOKEN")


@functions_framework.cloud_event
def execute_restore_agent(cloud_event: CloudEvent) -> None:
    """
    Executes the backup of a virtual agent.

    Args:
        event: The event triggering the backup (a Pub/Sub message).

    Returns:
        None

    Raises:
        ValueError: If the source_environment is invalid.
    """

    staging_bucket = os.getenv("STAGING_BUCKET_NAME")
    rejected_bucket = os.getenv("REJECTED_BUCKET_NAME")
    archive_bucket = os.getenv("ARCHIVE_BUCKET_NAME")

    agent_id = os.getenv("DIALOGFLOW_AGENT_ID")
    location = os.getenv("DIALOGFLOW_REGION")
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID")

    landing_bucket = cloud_event.data["bucket"]
    blob_path = cloud_event.data["name"]

    # move file to staging bucket
    move_file(
        source_bucket_name=landing_bucket,
        destination_bucket_name=staging_bucket,
        blob_path=blob_path,
    )

    try:
        # restore the agent from the staging bucket
        restore_agent(
            agent_id=f"projects/{project_id}/locations/{location}/agents/{agent_id}",
            bucket_name=staging_bucket,
            file_name=blob_path,
            location=location,
        )
        # check the id token for the agent
        check_id_token(agent_id=f"projects/{project_id}/locations/{location}/agents/{agent_id}")

        # move the file to the archive bucket
        move_file(
            source_bucket_name=staging_bucket,
            destination_bucket_name=archive_bucket,
            blob_path=blob_path,
        )
    except Exception as e:
        # move the file to the reject bucket
        move_file(
            source_bucket_name=staging_bucket,
            destination_bucket_name=rejected_bucket,
            blob_path=blob_path,
        )

        # give a complete log of the error
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    data = {
        "message": {
            "data": "SGVsbG8sIFdvcmxkIQ==",
            "attributes": {"source_environment": "QA"},
        },
        "bucket": "sandbox-jrubin-backup_agent_landing",
        "name": "agent-8a68761c-7f33-4472-a997-1d58b622b449-2024-07-18-15-48-QA-backup.blob",
        "metageneration": "1",
        "timeCreated": "2021-07-12T20:17:46.057Z",
        "updated": "2021-07-12T20:17:46.057Z",
    }

    attributes = {
        "type": "com.example.sampletype1",
        "source": "https://example.com/event-producer",
    }

    mock_cloud_event = CloudEvent(attributes, data)

    execute_restore_agent(mock_cloud_event)
