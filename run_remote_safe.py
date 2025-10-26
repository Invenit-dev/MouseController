#!/usr/bin/env python3
import os
import sys
import tempfile
import subprocess
import hashlib
import time
import requests

# CONFIG
RAW_FILE_URL = "https://raw.githubusercontent.com/Invenit-dev/MouseController/main/QT_ALL-QuotationList_v0.py"
COMMITS_API_URL = "https://api.github.com/repos/Invenit-dev/MouseController/commits/main"
EXEC_TIMEOUT = 300
VENV_PATH = os.path.expanduser("~/sandbox")
REQUIRED_PACKAGES = ["requests", "pyautogui", "pandas", "pyperclip"]

# --- Virtualenv ---
def ensure_virtualenv(path):
    if not os.path.exists(path):
        subprocess.check_call([sys.executable, "-m", "venv", path])
    return os.path.join(path, "bin", "python")
"""
def install_missing_packages(python_cmd, packages):
    for pkg in packages:
        try:
            subprocess.run([python_cmd, "-c", f"import {pkg}"], check=True)
        except subprocess.CalledProcessError:
            print(f"Installazione di {pkg}...")
            subprocess.check_call([python_cmd, "-m", "pip", "install", pkg])
"""
# --- Download ---
def download_file(url):
    url_bypass = f"{url}?t={int(time.time())}"
    headers = {"Cache-Control": "no-cache"}
    resp = requests.get(url_bypass, headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.content

def get_latest_commit_hash(api_url):
    resp = requests.get(api_url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data["sha"]

# --- Utility ---
def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()

def save_temp_py(data):
    tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
    tmp.write(data)
    tmp.flush()
    tmp.close()
    return tmp.name

def run_file_in_subprocess(python_cmd, path, timeout):
    env = os.environ.copy()
    cmd = [python_cmd, path]
    try:
        completed = subprocess.run(cmd, check=False, timeout=timeout, env=env)
        #print("Processo terminato con codice:", completed.returncode)
    except subprocess.TimeoutExpired:
        print(f"Timeout: il processo non ha terminato entro {timeout} secondi.")
    except Exception as e:
        print("Errore durante l'esecuzione:", e)

# --- Main ---
def main():
    python_cmd = ensure_virtualenv(VENV_PATH)
    #install_missing_packages(python_cmd, REQUIRED_PACKAGES)

    print("Scarico commit più recente della branch 'main'...")
    try:
        latest_commit = get_latest_commit_hash(COMMITS_API_URL)
        print("\tCommit hash:", latest_commit)
    except Exception as e:
        print("Errore ottenendo commit hash:", e)
        latest_commit = None

    print("Scarico ultima versione del file da GitHub...")
    try:
        data = download_file(RAW_FILE_URL)
    except Exception as e:
        print("Errore download:", e)
        sys.exit(1)

    h = sha256_hex(data)
    print("\tSHA256 del file scaricato:", h)

    tmp_path = save_temp_py(data)

    try:
        run_file_in_subprocess(python_cmd, tmp_path, EXEC_TIMEOUT)
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

if __name__ == "__main__":
    main()
