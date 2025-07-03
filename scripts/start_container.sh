#!/bin/bash
set -e

# --- Install AWS CLI if not already installed ---
if ! command -v aws &> /dev/null; then
  echo "AWS CLI not found. Installing..."
  apt update -y
  apt install unzip curl -y
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
  export PATH=$PATH:/usr/local/bin
fi

# --- Load values from AWS SSM Parameter Store ---
echo "Fetching Docker credentials from SSM..."

USERNAME=$(aws ssm get-parameter --name "/University-Project/docker/username" --with-decryption --query "Parameter.Value" --output text)
REGISTRY=$(aws ssm get-parameter --name "/University-Project/docker/registry" --with-decryption --query "Parameter.Value" --output text)

# --- Configuration ---
IMAGE_NAME="university-project"   
PORT=8003
FULL_IMAGE="$REGISTRY/$USERNAME/$IMAGE_NAME:latest"

# --- Pull latest image from Docker registry ---
echo "Pulling Docker image: $FULL_IMAGE"
docker pull "$FULL_IMAGE"

# --- Start the container ---
echo "Starting new container..."
docker run -d --name University-Project -p $PORT:8003 "$FULL_IMAGE"

# --- Confirm status ---
echo "Container '$FULL_IMAGE' started successfully on port $PORT."
docker ps --filter "name=University-Project"
