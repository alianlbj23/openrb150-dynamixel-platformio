#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import time
import argparse
import shutil
from pathlib import Path

# ============================================================
# Project path resolution (scheme B)
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent      # tools/
PROJECT_ROOT = (SCRIPT_DIR / "..").resolve()      # repo root
DEFAULT_FIRMWARE = PROJECT_ROOT / ".pio" / "build" / "OpenRB-150" / "firmware.bin"

# ============================================================
# Python venv config (Python deps only)
# ============================================================

VENV_DIR = PROJECT_ROOT / ".venv-openrb"
REQUIRED_PACKAGES = ["pyserial"]

# ============================================================
# Utils
# ============================================================

def run(cmd, check=True):
    print(">", " ".join(map(str, cmd)))
    return subprocess.run(cmd, check=check)


def is_venv():
    return (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
    )


def get_venv_python():
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def ensure_venv():
    """Ensure running inside venv with required Python packages."""
    if is_venv():
        return

    if not VENV_DIR.exists():
        print(f"[INFO] Creating venv: {VENV_DIR}")
        run([sys.executable, "-m", "venv", str(VENV_DIR)])

    py = get_venv_python()

    print("[INFO] Installing required packages in venv...")
    run([str(py), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(py), "-m", "pip", "install", *REQUIRED_PACKAGES])

    print("[INFO] Re-launching inside venv...")
    os.execv(str(py), [str(py)] + sys.argv)

# ============================================================
# bossac auto-detect (cross-platform)
# ============================================================

def resolve_bossac(cmd: str) -> str:
    """
    Resolve bossac executable path in the following order:
      1. Explicit path provided by user
      2. System PATH
      3. PlatformIO tool-bossac
    """
    # 1. Explicit path
    if os.path.sep in cmd and os.path.exists(cmd):
        return cmd

    # 2. System PATH
    found = shutil.which(cmd)
    if found:
        return found

    # 3. PlatformIO tool-bossac
    home = Path.home()
    if platform.system() == "Windows":
        pio_bossac = home / ".platformio" / "packages" / "tool-bossac" / "bossac.exe"
    else:
        pio_bossac = home / ".platformio" / "packages" / "tool-bossac" / "bossac"

    if pio_bossac.exists():
        print(f"[INFO] Using PlatformIO bossac: {pio_bossac}")
        return str(pio_bossac)

    return cmd  # will fail later with clear error

# ============================================================
# Upload logic
# ============================================================

def touch_1200bps(port):
    print(f"[INFO] 1200bps touch on {port}")
    try:
        import serial
        ser = serial.Serial(port, 1200)
        ser.close()
    except Exception as e:
        print(f"[WARN] 1200bps touch failed: {e}")


def upload_firmware(port, firmware, bossac="bossac",
                    do_touch=True, wait_s=2.0):

    firmware = Path(firmware)

    if not firmware.exists():
        print(f"[ERROR] Firmware not found: {firmware}")
        print(f"[DEBUG] cwd          : {os.getcwd()}")
        print(f"[DEBUG] project root : {PROJECT_ROOT}")
        print("[HINT ] Run compile first:")
        print("        python3 tools/compile_docker.py --verbose")
        return 2

    bossac = resolve_bossac(bossac)

    if platform.system() == "Windows" and not bossac.lower().endswith(".exe"):
        bossac += ".exe"

    if not shutil.which(bossac) and not os.path.exists(bossac):
        print("[ERROR] bossac not found.")
        print("Tried:")
        print("  - system PATH")
        print("  - PlatformIO tool-bossac")
        print("[HINT ] Install options:")
        print("  macOS  : brew install bossac")
        print("  Linux  : sudo apt install bossac")
        print("  Or use PlatformIO tool-bossac")
        return 127

    if do_touch:
        touch_1200bps(port)
        print("[INFO] Waiting for bootloader...")
        time.sleep(wait_s)

    cmd = [
        bossac,
        "-i",
        "-d",
        f"--port={port}",
        "-U", "true",
        "-e",
        "-w", str(firmware),
        "-R"
    ]

    try:
        run(cmd, check=True)
        print("[OK] Upload complete")
        return 0

    except subprocess.CalledProcessError as e:
        print("[ERROR] Upload failed (bossac returned non-zero).")
        return e.returncode or 1

# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="OpenRB-150 firmware uploader (host-side, no compile)"
    )
    parser.add_argument(
        "--port",
        required=True,
        help="USB serial port (e.g. /dev/cu.usbmodemXXXX, /dev/ttyACM0, COM5)"
    )
    parser.add_argument(
        "--firmware",
        default=str(DEFAULT_FIRMWARE),
        help="Firmware path (default: <repo>/.pio/build/OpenRB-150/firmware.bin)"
    )
    parser.add_argument(
        "--bossac",
        default="bossac",
        help="bossac command or path (auto-detect if not found)"
    )
    parser.add_argument(
        "--no-touch",
        action="store_true",
        help="Skip 1200bps touch/reset"
    )
    parser.add_argument(
        "--wait",
        type=float,
        default=2.0,
        help="Seconds to wait after touch (default: 2.0)"
    )

    args = parser.parse_args()

    ensure_venv()

    return upload_firmware(
        port=args.port,
        firmware=args.firmware,
        bossac=args.bossac,
        do_touch=(not args.no_touch),
        wait_s=args.wait
    )


if __name__ == "__main__":
    raise SystemExit(main())
