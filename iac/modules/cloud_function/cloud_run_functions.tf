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
      for_each = each.value.secret_env_vars
      content {
        project_id = var.project_id
        key        = secret_environment_variables.value.key
        secret     = secret_environment_variables.value.secret
        version    = secret_environment_variables.value.version
      }
    }
    # secret_environment_variables {
    #   key        = "CLOUD_SQL_SECRET"
    #   project_id = var.project_id
    #   secret     = google_secret_manager_secret.cloud_sql_secret.secret_id
    #   version    = "latest"
    # }
  }
}
