# Terraform for Dialogflow CX Webhook Deployment

This Terraform project automates the deployment of a Dialogflow CX webhook to Google Cloud Functions.

## Prerequisites

* **Google Cloud Project:**  A GCP project with billing enabled.
* **Terraform:** Installed and configured on your local machine.
* **Google Cloud SDK:**  Installed and configured with appropriate credentials.

## Usage

1. **Clone Repository:** Clone this repository to your local machine.

2. **Set Variables:**  Edit the `variables.tf` file to configure the following variables:

    * `project_id`: Your Google Cloud project ID.
    * `region`: The GCP region where you want to deploy the function (e.g., `europe-west1`).
    * `function_name`: The name of the Cloud Function.
    * `function_entry_point`: The entry point function in your code (e.g., `webhook_entrypoint`).
    * `environment`: The environment you are deploying to (e.g., `poc`, `prod`).  This is used for naming resources.


3. **Initialize Terraform:** Run `sh ./terraform_init` to initialize the project and download necessary providers.

4. **Plan:** Run `sh ./terraform plan poc` to preview the changes that will be applied.

5. **Apply:** Run `sh ./terraform_apply poc` to deploy the resources.


## Modules

This project uses modules for better organization:

* **`modules/apis`:** Enables the required Google Cloud APIs.
* **`modules/resources`:** Creates the Cloud Function, Cloud Storage bucket for state, and other related resources.


## State Management

This project uses a Google Cloud Storage bucket for remote state management. The bucket name is dynamically generated based on your project ID (`<project_id>-pi-electronics-tf-state`).

## Outputs

The following output is available after successful deployment:

* `project_id`: The project ID used for the deployment.


## Cleanup

To destroy the deployed resources, run `terraform destroy`.

## Note

- Ensure that the required APIs are enabled in your Google Cloud project before running Terraform.
- Make sure your Cloud Function code is located in the appropriate directory and the `function_entry_point` variable is set correctly.
- This setup includes a remote backend for Terraform state.  If you're working in a team, ensure everyone uses the same backend configuration.


## Further Improvements

* **IAM:** Fine-tune IAM permissions for least privilege access.
* **Environment Variables:**  Use environment variables to manage sensitive configuration within the Cloud Function.
* **Automated Testing:** Integrate automated testing into your deployment pipeline.
