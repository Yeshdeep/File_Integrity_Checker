import os
import hashlib
import json
from datetime import datetime

BASELINE_FILE = "baseline.json"
LOG_FILE = "integrity_log.txt"


def calculate_hash(file_path):
    """
    Calculate SHA256 hash of a file in chunks (memory efficient).
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def create_baseline(directory):
    """
    Create a baseline (hash values of all files in a directory).
    """
    baseline_data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            baseline_data[file_path] = calculate_hash(file_path)

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline_data, f, indent=4)

    print(f"✔️ Baseline created and saved to {BASELINE_FILE}")


def log_message(message):
    """
    Save logs with timestamps into integrity_log.txt.
    """
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")


def check_integrity(directory):
    """
    Compare current file hashes with baseline and log results.
    """
    if not os.path.exists(BASELINE_FILE):
        print("❌ No baseline found. Please create one first.")
        return

    with open(BASELINE_FILE, "r") as f:
        baseline_data = json.load(f)

    current_data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            current_data[file_path] = calculate_hash(file_path)

    print("\n🔍 Checking integrity...\n")

    # Track changes
    for file_path, old_hash in baseline_data.items():
        if file_path not in current_data:
            msg = f"[DELETED] {file_path}"
            print(f"❌ {msg}")
            log_message(msg)
        elif current_data[file_path] != old_hash:
            msg = f"[MODIFIED] {file_path}"
            print(f"⚠️ {msg}")
            log_message(msg)

    for file_path in current_data:
        if file_path not in baseline_data:
            msg = f"[NEW] {file_path}"
            print(f"➕ {msg}")
            log_message(msg)

    print("\n✔️ Integrity check complete. Results saved in integrity_log.txt\n")


def main():
    print("===== 🛡️ File Integrity Checker =====")
    print("1️⃣ Create Baseline (first time setup)")
    print("2️⃣ Check Integrity (compare with baseline)")
    print("3️⃣ Exit")

    choice = input("\nEnter choice (1/2/3): ").strip()

    if choice == "3":
        print("👋 Exiting program. Goodbye!")
        return

    target_dir = input("📂 Enter directory path to monitor: ").strip()

    if not os.path.exists(target_dir):
        print("❌ Error: Directory does not exist.")
        return

    if choice == "1":
        create_baseline(target_dir)
    elif choice == "2":
        check_integrity(target_dir)
    else:
        print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
