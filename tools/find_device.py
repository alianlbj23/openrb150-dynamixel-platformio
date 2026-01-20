#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
from serial.tools import list_ports

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

def main():
    ensure_venv()

    

    ports = list(list_ports.comports())
    if not ports:
        print("(none)")
        return 0

    # macOS/Linux: /dev/xxx；Windows: COMx
    print()
    print("=================================")
    for p in ports:
        dev = p.device
        desc = (p.description or "").strip()
        hwid = (p.hwid or "").strip()

        if platform.system() in ("Darwin", "Linux"):
            if dev.startswith("/dev/"):
                print(f"{dev} | {desc}")
        else:
            # Windows 沒有 /dev，就列 COM + 裝置名稱
            print(f"{dev} | {desc} | {hwid}")
    print("=================================")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
