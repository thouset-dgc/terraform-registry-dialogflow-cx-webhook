
module "gcp_cloud_functions" {
  source                         = "./modules/cloud_function"
  project_id                     = var.project_id
  region                         = var.region
  cloud_run_function_bucket_name = google_storage_bucket.cloud_run_function_sources.name
  cloud_run_functions_setting = {
    webhook_function = {
      function_name         = "dialogflow-cx-webhook"
      function_description  = "My GCP Cloud Function used as webhook for Dialogflow CX"
      function_entry_point  = "webhook_entrypoint"
      min_instance_count    = 1
      memory                = "256M"
      timeout               = 360
      ingress_settings      = "ALLOW_ALL"
      service_account_email = google_service_account.service_account["df-webhook-${var.project_id}"].email
      environment_vars = {
        PROJECT_ID    = var.project_id
        REGION        = var.region
        LOG_EXECUTION = true
      }
      secret_env_vars = [
        {
          key     = "CLOUD_SQL_SECRET"
          secret  = google_secret_manager_secret.secret["cloud-sql-secret"].secret_id
          version = "latest"
        }
      ]
      source_dir  = "../cloud_function/webhook/src/"
      output_path = "../cloud_function_zip/webhook"
    }
    hello_world_function = {
      function_name         = "ingestion"
      function_description  = "My GCP ingestion world Cloud Function"
      function_entry_point  = "ingestion_entry"
      min_instance_count    = 1
      memory                = "256M"
      timeout               = 360
      ingress_settings      = "ALLOW_ALL"
      service_account_email = google_service_account.service_account["df-webhook-${var.project_id}"].email
      environment_vars = {
        PROJECT_ID    = var.project_id
        REGION        = var.region
        LOG_EXECUTION = true
      }
      event_trigger = {
        trigger_region = var.region
        event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
        pubsub_topic   = google_pubsub_topic.topics["export-agent"].id
        retry_policy   = "RETRY_POLICY_DO_NOT_RETRY"
      }
      source_dir  = "../cloud_function/ingestion/src/"
      output_path = "../cloud_function_zip/ingestion"
    }
  }
}
# event_trigger = optional(object({
#       trigger_region = string
#       event_type     = string
#       event_filter = optional(object({
#         attribute = string
#         value     = string
#       }))
#       pubsub_topic = optional(string)
#       retry_policy = string
#     }))
