#!/usr/bin/env bash
set -euo pipefail

# This script builds the development environment Docker image (always linux/amd64).

# --- Configuration ---
IMAGE_NAME="${IMAGE_NAME:-openrb150-dev-env:latest}"
DOCKER_PLATFORM="${DOCKER_PLATFORM:-linux/amd64}"

# Project root (parent directory of this script)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Project root (build context): ${PROJECT_ROOT}"
echo "Dockerfile path: ${PROJECT_ROOT}/docker/Dockerfile"
echo "Host arch: $(uname -m)"
echo "Target platform: ${DOCKER_PLATFORM}"
echo "Image tag: ${IMAGE_NAME}"
echo ""

# --- Ensure buildx is available ---
if ! docker buildx version >/dev/null 2>&1; then
  echo "Error: docker buildx is not available."
  echo "Please enable BuildKit/buildx (Docker Desktop usually includes it)."
  exit 1
fi

# --- Build the Docker Image ---
echo "Building Docker image '${IMAGE_NAME}' for platform ${DOCKER_PLATFORM}..."

docker buildx build \
  --platform "${DOCKER_PLATFORM}" \
  --load \
  -t "${IMAGE_NAME}" \
  -f "${PROJECT_ROOT}/docker/Dockerfile" \
  "${PROJECT_ROOT}"

echo ""
echo "Docker image '${IMAGE_NAME}' built successfully."
echo "Next:"
echo "  ./docker/run.sh"
