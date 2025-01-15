
variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
}

variable "cloud_run_function_bucket_name" {
  description = "The name of the bucket to store Cloud Functions sources"
  type        = string
}

variable "cloud_run_functions_setting" {
  description = "Liste des fonctions à déployer avec leurs paramètres."
  type = map(object({
    function_name         = string
    function_description  = string
    function_entry_point  = string
    min_instance_count    = number #(Ex: 1)
    memory                = string #(Ex:"256M")
    timeout               = number #(Ex: 360)
    ingress_settings      = string #(Ex: "ALLOW")
    service_account_email = string
    environment_vars      = map(any) #(Ex:  {LOG_EXECUTION_ID= true PROJECT_ID = var.project_id PROJECT_REGION = var.region PROJECT_CLOUD_SQL_INSTANCE = "chatbot"}
    secret_env_vars = list(object({
      key     = string
      secret  = string
      version = string
    }))
    source_dir  = string
    output_path = string

  }))
}

