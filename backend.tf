terraform {
  required_version = ">= 0.15"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.14.1"
    }
  }
  backend "gcs" {
    bucket = "MY_PROJECT-tf-state"
  }
}
