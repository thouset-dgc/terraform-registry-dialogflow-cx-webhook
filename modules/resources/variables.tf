variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "project_number" {
  description = "The GCP project number"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
}

variable "function_name" {
  description = "Name of the Cloud Function"
  type        = string
}

variable "function_entry_point" {
  description = "Entry point of the Cloud Function"
  type        = string
}

variable "environment" {
  description = "environment"
  type        = string
}
