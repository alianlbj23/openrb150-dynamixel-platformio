#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import time
import argparse

VENV_DIR = ".venv-openrb"
REQUIRED_PACKAGES = ["pyserial"]


def run(cmd, check=True, capture=False, text=True):
    if isinstance(cmd, str):
        print(">", cmd)
        return subprocess.run(cmd, shell=True, check=check, capture_output=capture, text=text)
    else:
        print(">", " ".join(cmd))
        return subprocess.run(cmd, check=check, capture_output=capture, text=text)


def is_venv():
    return (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
    )


def get_venv_python():
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")


def ensure_venv():
    if is_venv():
        return

    if not os.path.exists(VENV_DIR):
        print(f"[INFO] Creating venv: {VENV_DIR}")
        run([sys.executable, "-m", "venv", VENV_DIR])

    py = get_venv_python()

    print("[INFO] Installing required packages in venv...")
    run([py, "-m", "pip", "install", "--upgrade", "pip"])
    run([py, "-m", "pip", "install", *REQUIRED_PACKAGES])

    print("[INFO] Re-launching inside venv...")
    os.execv(py, [py] + sys.argv)


def touch_1200bps(port):
    print(f"[INFO] 1200bps touch on {port}")
    try:
        import serial
        ser = serial.Serial(port, 1200)
        ser.close()
    except Exception as e:
        print(f"[WARN] 1200bps touch failed: {e}")


def upload_firmware(port, firmware, bossac="bossac", do_touch=True, wait_s=2.0):
    if not os.path.exists(firmware):
        print(f"[ERROR] Firmware not found: {firmware}")
        return 2

    if platform.system() == "Windows" and not bossac.lower().endswith(".exe"):
        bossac = bossac + ".exe"

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
        "-w", firmware,
        "-R"
    ]

    try:
        run(cmd, check=True)
        print("[OK] Upload complete")
        return 0
    except subprocess.CalledProcessError as e:
        print("[ERROR] Upload failed (bossac returned non-zero).")
        return e.returncode or 1
    except FileNotFoundError:
        print("[ERROR] bossac not found in PATH.")
        print("  - macOS: brew install bossac")
        print("  - Linux: sudo apt install bossac")
        print("  - Windows: install Arduino SAMD tools and add bossac.exe to PATH")
        return 127


def main():
    parser = argparse.ArgumentParser(description="OpenRB-150 uploader (bossac)")
    parser.add_argument("--port", required=True, help="USB serial port (e.g. /dev/cu.usbmodem1101, /dev/ttyACM0, COM5)")
    parser.add_argument("--firmware", default=".pio/build/OpenRB-150/firmware.bin", help="Firmware path")
    parser.add_argument("--bossac", default="bossac", help="bossac command (default: bossac)")
    parser.add_argument("--no-touch", action="store_true", help="Skip 1200bps touch/reset")
    parser.add_argument("--wait", type=float, default=2.0, help="Seconds to wait after touch (default: 2.0)")
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
