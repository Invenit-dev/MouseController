#!/usr/bin/env python3
"""
Scarica ed esegue uno script Python da GitHub (raw).
Mostra l'hash SHA256 e richiede conferma via input prima di eseguire.
Esegue il file in un processo separato con timeout opzionale.
"""

import requests
import tempfile
import hashlib
import subprocess
import sys
import os

# === CONFIG ===
# URL "raw" del file su GitHub (cambia se necessario)
URL = "https://raw.githubusercontent.com/Invenit-dev/MouseController/main/QT_ALL-QuotationList_v0.py"

# Timeout in secondi per l'esecuzione (None = nessun timeout)
EXEC_TIMEOUT = 60

# Comando Python da usare (es. "python3" o "python")
#PYTHON_CMD = sys.executable  # usa lo stesso interprete che lancia questo script
PYTHON_CMD = os.path.expanduser("~/sandbox/bin/python")

# =================

def download(url: str) -> bytes:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.content

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def save_temp_py(data: bytes) -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
    try:
        tmp.write(data)
        tmp.flush()
        return tmp.name
    finally:
        tmp.close()

def run_file_in_subprocess(path: str, timeout: int | None):
    # Esegui in un nuovo processo per isolamento (puoi aggiungere env limitati)
    env = os.environ.copy()
    # opzionale: svuota env o mantieni solo variabili essenziali
    # env = {"PATH": env.get("PATH", "")}
    cmd = [PYTHON_CMD, path]
    print("Eseguo:", " ".join(cmd))
    try:
        completed = subprocess.run(cmd, check=False, timeout=timeout, env=env)
        print("Processo terminato con codice:", completed.returncode)
    except subprocess.TimeoutExpired:
        print(f"Timeout: il processo non ha terminato entro {timeout} secondi.")
    except Exception as e:
        print("Errore durante l'esecuzione:", e)

def main():
    print("Scarico:", URL)
    try:
        data = download(URL)
    except Exception as e:
        print("Errore download:", e)
        sys.exit(1)

    h = sha256_hex(data)
    print("SHA256 del file scaricato:", h)
    print()
    print("Attenzione: assicurati che l'hash corrisponda all'hash atteso del file su GitHub.")
    ans = input("Vuoi procedere con l'esecuzione del file scaricato? (s/N) ").strip().lower()
    if ans != "s":
        print("Annullato dall'utente.")
        # opzionale: salva il file per ispezione
        tmp_path = save_temp_py(data)
        print("File salvato per ispezione in:", tmp_path)
        sys.exit(0)

    # salva e esegui
    tmp_path = save_temp_py(data)
    print("File salvato temporaneamente in:", tmp_path)

    try:
        run_file_in_subprocess(tmp_path, EXEC_TIMEOUT)
    finally:
        # opzionale: rimuovere file temporaneo
        try:
            os.remove(tmp_path)
        except Exception:
            pass

if __name__ == "__main__":
    main()
