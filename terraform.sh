#!/bin/bash


# Check if an environment is provided
if [ -z "$1" ]; then
    echo "Error: Please specify an environment (e.g., sh terraform.sh poc)"
    exit 1
fi

cd iac

ENVIRONMENT=$1

# Set Project ID based on environment
if [ "$ENVIRONMENT" == "poc" ]; then
    VARIABLES_FILE="env/$ENVIRONMENT.tfvars"
    PROJECT_ID=$(grep -E '^project_id' "$VARIABLES_FILE" | awk -F'=' '{print $2}' | tr -d ' "')
    echo "PROJECT_ID : $PROJECT_ID"

else
    echo "Invalid environment"
    exit 1
fi

#export USER_PROJECT_OVERRIDE=True
# export PROJECT_ID=$PROJECT_ID 
# export GOOGLE_CLOUD_QUOTA_PROJECT=$PROJECT_ID


# Initialize Terraform (only if not already initialized)
if [[ ! -f .terraform/environment ]]; then # Check for .terraform directory or other suitable check
    
    BACKEND_FILE="backend/backend_$ENVIRONMENT.tfvars"
    echo "$PWD/$BACKEND_FILE"
    #gcloud auth list
   
    terraform init -upgrade -backend-config="$BACKEND_FILE" -reconfigure
    #terraform init -upgrade -backend-config="$BACKEND_FILE"

    if [[ $? -ne 0 ]]; then
        echo "Error: terraform init failed"
        exit 1
    fi
fi

# Terraform plan
terraform plan -out=tfplan.$ENVIRONMENT -var-file="env/$ENVIRONMENT.tfvars"
if [[ $? -ne 0 ]]; then
    echo "Error: terraform plan failed"
    exit 1
fi

read -p "Apply Terraform plan? (yes/no): " CHOICE

if [[ "$CHOICE" == "yes" ]]; then
    terraform apply tfplan.$ENVIRONMENT

    if [[ $? -ne 0 ]]; then
        echo "Error: terraform apply failed"
        exit 1
    fi

    rm tfplan.$ENVIRONMENT 

else
    echo "Terraform apply cancelled."
fi

cd ..
rm -rf cloud_function_zip/* # remove zip generated file