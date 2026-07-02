import os
import sys
from kaggle.api.kaggle_api_extended import KaggleApi
from scripts.preprocessing import run_preprocessing_pipeline
import pandas as pd
import hashlib

DATASET_ID = "ahmad03038/cristiano-ronaldo-youtube-stats-data-daily-pull"
RAW_DATA_PATH = "data/cristiano_youtube_stats.csv"
PROCESSED_DATA_PATH = "data/processed_data.parquet"


def get_file_hash(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def should_update(local_path, remote_file_metadata):
    if not os.path.exists(local_path):
        return True
    
    local_size = os.path.getsize(local_path)
    return local_size != remote_file_metadata.sizeInBytes


def main():
    # 1. Authenticate
    api = KaggleApi()
    api.authenticate()

    # 2. Check for updates
    # List files to get metadata
    files = api.dataset_list_files(DATASET_ID).files
    target_file = next(
        (f for f in files if f.name == "cristiano_youtube_stats.csv"), None
    )

    if target_file is None:
        print("Error: Could not find dataset file on Kaggle.")
        sys.exit(1)

    # Use refactored logic
    if not should_update(RAW_DATA_PATH, target_file):
        print("No changes detected in remote dataset size. Skipping update.")
        sys.exit(0)

    # 3. Download the dataset directly to data/
    print(f"Downloading dataset {DATASET_ID}...")
    api.dataset_download_files(DATASET_ID, path="data", unzip=True)

    # 4. Run preprocessing
    print("Running preprocessing pipeline...")
    raw_df = pd.read_csv(RAW_DATA_PATH)
    processed_df = run_preprocessing_pipeline(raw_df)

    # 5. Save processed data
    processed_df.to_parquet(PROCESSED_DATA_PATH, index=False)
    print(f"Dataset updated and processed in {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    main()
