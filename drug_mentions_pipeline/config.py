"""
Configuration settings for the drug mentions pipeline.
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Input data paths
INPUT_DIR = DATA_DIR / "input"
DRUGS_PATH = INPUT_DIR / "drugs.csv"
PUBMED_CSV_PATH = INPUT_DIR / "pubmed.csv"
PUBMED_JSON_PATH = INPUT_DIR / "pubmed.json"
CLINICAL_TRIALS_PATH = INPUT_DIR / "clinical_trials.csv"

# Output data paths
OUTPUT_DIR = DATA_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "drug_graph.json"

# Create directories if they don't exist
for directory in [INPUT_DIR, OUTPUT_DIR]:
    os.makedirs(directory, exist_ok=True)

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"