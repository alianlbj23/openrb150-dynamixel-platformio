#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-openrb150-dev-env:latest}"
CONTAINER_NAME="${CONTAINER_NAME:-openrb150-dev}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# For atmelsam toolchain support, always run amd64 container
PIO_PLATFORM="${PIO_PLATFORM:-linux/amd64}"

# Detect OS
HOST_OS="$(uname -s)"

# Optional: detect serial device (Linux only; macOS Docker USB passthrough is unreliable)
SERIAL_DEV="${SERIAL_DEV:-}"
if [[ "${HOST_OS}" == "Linux" && -z "${SERIAL_DEV}" ]]; then
  for d in /dev/ttyACM0 /dev/ttyACM1 /dev/ttyUSB0 /dev/ttyUSB1; do
    if [[ -e "$d" ]]; then
      SERIAL_DEV="$d"
      break
    fi
  done
fi

# Check image exists
if ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
  echo "Error: Docker image '${IMAGE_NAME}' not found."
  echo "Please build it first by running: ./docker/build.sh"
  exit 1
fi

echo "Starting container '${CONTAINER_NAME}'..."
echo "Project mounted at /workspace"
echo "Container platform: ${PIO_PLATFORM}"
echo "Host OS: ${HOST_OS}"
if [[ -n "${SERIAL_DEV}" ]]; then
  echo "Serial device (Linux): ${SERIAL_DEV}"
fi
echo
echo "Inside container, build with:"
echo "  pio run -e OpenRB-150 -v"
echo "Exit with Ctrl+D or 'exit'"
echo
echo "Upload recommendation:"
echo "  Run upload on host (macOS/Linux): pio run -e OpenRB-150 -t upload -v"
echo

RUN_ARGS=( -it --rm
  --name "${CONTAINER_NAME}"
  --platform "${PIO_PLATFORM}"
  -v "${PROJECT_ROOT}:/workspace"
  -w /workspace
)

# Only pass serial device into container on Linux (optional)
if [[ "${HOST_OS}" == "Linux" && -n "${SERIAL_DEV}" ]]; then
  RUN_ARGS+=( --device "${SERIAL_DEV}:${SERIAL_DEV}" )
fi

docker run "${RUN_ARGS[@]}" "${IMAGE_NAME}" /bin/bash
echo "Container stopped."
