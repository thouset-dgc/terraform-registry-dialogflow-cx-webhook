variable "project_id" {
  type        = string
  description = "Project identifier"
  default     = "gcp-project-id"
}

variable "project_number" {
  type        = string
  description = "Project identifier"
  default     = "12312312"
}

variable "location" {
  description = "GCP location"
  type        = string
  default     = "eu"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west1"
}

variable "repository_name" {
  description = "The name of the repository"
  type        = string

}

variable "owner" {
  description = "The repository owner"
  type        = string
}

variable "function_name" {
  description = "Name of the Cloud Function"
  type        = string
  default     = "dialogflow-cx-webhook"
}

variable "function_entry_point" {
  description = "Entry point of the Cloud Function"
  type        = string
  default     = "webhook_entrypoint"
}

variable "environment" {
  description = "Environment of code"
  type        = string

}
