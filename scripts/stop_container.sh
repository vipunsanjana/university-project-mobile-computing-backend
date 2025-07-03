#!/bin/bash
set -e  # Exit on any error

echo "Stopping all running Docker containers..."

# Get all running container IDs (excluding header)
RUNNING_CONTAINERS=$(docker ps -q)

if [ -n "$RUNNING_CONTAINERS" ]; then
  echo "$RUNNING_CONTAINERS" | xargs docker stop
  echo "All running containers stopped."
else
  echo "No running containers to stop."
fi

echo "Removing all containers..."

# Get all container IDs (running + exited)
ALL_CONTAINERS=$(docker ps -aq)

if [ -n "$ALL_CONTAINERS" ]; then
  echo "$ALL_CONTAINERS" | xargs docker rm
  echo "All containers removed."
else
  echo "No containers to remove."
fi

echo "Docker cleanup complete."
