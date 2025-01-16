#!/bin/bash


#export PROJECT_ID=$(gcloud info --format='value(config.project)')

# Set the bucket location (e.g., 'us', 'eu', 'asia')
#export BUCKET_LOCATION=eu  # Specify your bucket location here

# Set the environment (e.g., 'dv', 'qa', 'pd')

# Define the Terraform bucket name using the project ID
PROJECT_ID="$1"
BUCKET_LOCATION="$2"
ENV="$3"


TERRAFORM_BUCKET="${PROJECT_ID}-rbs-chatbot-gcs-tfstate"

# Display project information
echo "******"
echo "Project ID value: $PROJECT_ID"
echo "Backend Terraform bucket: $TERRAFORM_BUCKET"
echo "Bucket location: $BUCKET_LOCATION"
echo "Environment: $ENV"
echo "******"

# Check if the bucket exists
gsutil ls -b -p $PROJECT_ID gs://$TERRAFORM_BUCKET || gsutil mb -l $BUCKET_LOCATION -p $PROJECT_ID gs://$TERRAFORM_BUCKET || gsutil versioning set on gs://$TERRAFORM_BUCKET 

# Write the bucket name to backend.tfvars
cd ../backend
echo "bucket = \"$TERRAFORM_BUCKET\"" > backend_${ENV}.tfvars
