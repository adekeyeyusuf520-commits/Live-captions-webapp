# download_vosk_wasm.py

import os
import zipfile
import urllib.request

# -----------------------------
# CONFIG
# -----------------------------
# URL of the Vosk WASM model (adjust if a new version is released)
zip_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-wasm.zip"
zip_path = "vosk_model_wasm.zip"
model_folder = "wasm_model"  # folder where model will be extracted

# -----------------------------
# Step 1: Create model folder if it doesn't exist
# -----------------------------
if not os.path.exists(model_folder):
    os.makedirs(model_folder)

# -----------------------------
# Step 2: Download the ZIP if not already downloaded
# -----------------------------
if not os.path.exists(zip_path):
    print("Downloading Vosk WASM model (~50MB)...")
    urllib.request.urlretrieve(zip_url, zip_path)
    print("Download complete!")
else:
    print("ZIP already exists, skipping download.")

# -----------------------------
# Step 3: Extract the ZIP
# -----------------------------
print("Extracting model...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(model_folder)
print(f"Model extracted to '{model_folder}' folder.")

# -----------------------------
# Step 4: Clean up ZIP (optional)
# -----------------------------
os.remove(zip_path)
print("Temporary ZIP removed. WASM model is ready!")
