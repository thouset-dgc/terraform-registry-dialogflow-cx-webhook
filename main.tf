module "gcp_apis" {
  source     = "./modules/apis"
  project_id = var.project_id
  apis = [
    "iam.googleapis.com",
    "cloudfunctions.googleapis.com",
    "storage.googleapis.com",
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "dialogflow.googleapis.com",
    "secretmanager.googleapis.com"
  ]
}

module "gcp_resources" {
  source               = "./modules/resources"
  project_id           = var.project_id
  project_number       = var.project_number
  environment          = var.environment
  region               = var.region
  function_name        = var.function_name
  function_entry_point = var.function_entry_point

  depends_on = [module.gcp_apis]
}
