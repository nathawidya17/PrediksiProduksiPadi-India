import json
import joblib
import sklearn
import sys
import os

def load_json_files():
    """Load state→district and season list from JSON."""
    with open("data/state_district.json") as f:
        state_dist = json.load(f)

    with open("data/season_list.json") as f:
        seasons = json.load(f)

    return state_dist, seasons


def load_all_models():
    """Load model, scaler, encoder + validate version compatibility."""

    MODEL_DIR = "models"

    # === LOAD METADATA ===
    metadata_path = os.path.join(MODEL_DIR, "metadata.pkl")

    print("Loading metadata.pkl...")
    metadata = joblib.load(metadata_path)

    saved_py = metadata.get("python_version", "unknown")
    saved_skl = metadata.get("sklearn_version", "unknown")

    print("\n=== VERSION CHECK ===")
    print(f"Saved Python version   : {saved_py}")
    print(f"Saved Sklearn version  : {saved_skl}")
    print(f"Current Python version : {sys.version.split()[0]}")
    print(f"Current Sklearn ver    : {sklearn.__version__}")

    # Tampilkan warning jika beda
    if sklearn.__version__ != saved_skl:
        print("\n⚠ WARNING: Sklearn version mismatch!")
        print("   Model may still load, but re-training is recommended.\n")

    # === LOAD MODEL ===
    print("Loading model.pkl...")
    model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))

    # === LOAD SCALER ===
    print("Loading minmax.pkl...")
    scaler = joblib.load(os.path.join(MODEL_DIR, "minmax.pkl"))

    # === LOAD LABEL ENCODER ===
    print("Loading labelencode.pkl...")
    encoder = joblib.load(os.path.join(MODEL_DIR, "labelencode.pkl"))

    print("\n✔ All models loaded successfully.\n")

    return model, scaler, encoder
