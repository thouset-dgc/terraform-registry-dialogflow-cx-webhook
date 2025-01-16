resource "google_cloudfunctions2_function" "cloud_function" {
  for_each    = var.cloud_run_functions_setting
  name        = each.value.function_name
  location    = var.region
  description = each.value.function_description

  build_config {
    runtime     = "python310"
    entry_point = each.value.function_entry_point

    source {
      storage_source {
        bucket = google_storage_bucket_object.function_zip[each.key].bucket
        object = google_storage_bucket_object.function_zip[each.key].name
      }
    }
  }

  service_config {
    min_instance_count = each.value.min_instance_count
    available_memory   = each.value.memory
    timeout_seconds    = each.value.timeout
    ingress_settings   = each.value.ingress_settings

    service_account_email = each.value.service_account_email

    environment_variables = each.value.environment_vars

    dynamic "secret_environment_variables" {
      for_each = each.value.secret_env_vars != null ? each.value.secret_env_vars : []
      content {
        project_id = var.project_id
        key        = secret_environment_variables.value.key
        secret     = secret_environment_variables.value.secret
        version    = secret_environment_variables.value.version
      }
    }

  }
  dynamic "event_trigger" {
    for_each = each.value.event_trigger != null ? [each.value.event_trigger] : []
    content {
      trigger_region = event_trigger.value.trigger_region
      event_type     = event_trigger.value.event_type
      dynamic "event_filters" {
        for_each = event_trigger.value.event_filter != null ? [event_trigger.value.event_filter] : []
        content {
          attribute = event_filters.value.attribute
          value     = event_filters.value.value
        }
      }
      pubsub_topic = event_trigger.value.pubsub_topic != null ? event_trigger.value.pubsub_topic : null
      retry_policy = event_trigger.value.retry_policy
    }
  }
}
