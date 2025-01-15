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
