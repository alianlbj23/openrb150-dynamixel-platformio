#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import argparse

DEFAULT_IMAGE_NAME = os.environ.get("IMAGE_NAME", "openrb150-dev-env:latest")
DEFAULT_CONTAINER_NAME = os.environ.get("CONTAINER_NAME", "openrb150-dev-compile")
DEFAULT_PIO_PLATFORM = os.environ.get("PIO_PLATFORM", "linux/amd64")


def sh(cmd: list[str], check=True) -> subprocess.CompletedProcess:
    print(">", " ".join(cmd))
    return subprocess.run(cmd, check=check)


def docker_image_exists(image: str) -> bool:
    try:
        subprocess.run(
            ["docker", "image", "inspect", image],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def repo_root_from_script() -> Path:
    # tools/compile_docker.py -> repo root is tools/..
    return (Path(__file__).resolve().parent / "..").resolve()


def main():
    parser = argparse.ArgumentParser(description="Compile OpenRB-150 firmware inside Docker (compile only)")
    parser.add_argument("--image", default=DEFAULT_IMAGE_NAME, help="Docker image name")
    parser.add_argument("--name", default=DEFAULT_CONTAINER_NAME, help="Docker container name")
    parser.add_argument("--platform", default=DEFAULT_PIO_PLATFORM, help="Docker platform (default: linux/amd64)")
    parser.add_argument("--env", default="OpenRB-150", help="PlatformIO env name (default: OpenRB-150)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose build output")
    args = parser.parse_args()

    repo_root = repo_root_from_script()

    if not docker_image_exists(args.image):
        print(f"[ERROR] Docker image '{args.image}' not found.")
        print("Build it first, e.g.: ./docker/build.sh")
        return 1

    pio_cmd = f"pio run -e {args.env}" + (" -v" if args.verbose else "")
    cmd_inside = f"set -e; {pio_cmd}; echo; echo '[OK] Build done. Artifacts are in .pio/build/{args.env}/ on host.'"

    run_args = [
        "docker", "run",
        "--rm",
        "--name", args.name,
        "--platform", args.platform,
        "-v", f"{str(repo_root)}:/workspace",
        "-w", "/workspace",
        args.image,
        "/bin/bash", "-lc", cmd_inside,
    ]

    print("[INFO] Compiling inside Docker...")
    print(f"[INFO] Repo: {repo_root}")
    print(f"[INFO] Image: {args.image}")
    print(f"[INFO] Env: {args.env}")
    sh(run_args, check=True)

    # Quick sanity check: firmware exists on host after compile
    firmware_bin = repo_root / ".pio" / "build" / args.env / "firmware.bin"
    if firmware_bin.exists():
        print(f"[OK] firmware.bin ready: {firmware_bin}")
        return 0

    # Some envs output .elf/.hex only; tell user where to look
    print("[WARN] firmware.bin not found. Check build output folder:")
    print(f"       {repo_root / '.pio' / 'build' / args.env}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
