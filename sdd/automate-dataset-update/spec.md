# Dataset Automation Specification

## Purpose

Automate the daily update of the dataset using the Kaggle API and GitHub Actions.

## Requirements

### Requirement: Kaggle Dataset Synchronization

The system SHALL automatically check for updates on Kaggle and synchronize the local dataset.

#### Scenario: Successful Update
- GIVEN the Kaggle API is configured correctly
- WHEN the daily cron job triggers the update script
- THEN the dataset is fetched and preprocessed
- AND the changes are committed and pushed to the repository

### Requirement: Idempotent Preprocessing

The preprocessing script MUST handle existing data gracefully, ensuring no duplicate or corrupted entries occur if run multiple times.

#### Scenario: No Changes Detected
- GIVEN the remote dataset has not changed since the last update
- WHEN the update script runs
- THEN the script completes without modifying files
- AND no new commit is generated

### Requirement: Credential Management and Error Handling

The system MUST securely manage Kaggle credentials and handle failures gracefully.

#### Scenario: Credential Failure
- GIVEN invalid or missing Kaggle API credentials
- WHEN the workflow executes
- THEN the process exits with a non-zero status code
- AND an error log is generated, but the repository remains in a consistent state

## Technical Design

### Workflow Structure (GitHub Action)

The workflow will reside in `.github/workflows/update-dataset.yml`:

```yaml
name: Update Dataset
on:
  schedule:
    - cron: '0 0 * * *' # Daily at midnight
  workflow_dispatch: # Allow manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install kaggle
      - name: Run update script
        env:
          KAGGLE_USERNAME: ${{ secrets.KAGGLE_USERNAME }}
          KAGGLE_KEY: ${{ secrets.KAGGLE_KEY }}
        run: python scripts/update_dataset.py
      - name: Commit and push changes
        run: |
          git config --global user.name "GitHub Action"
          git config --global user.email "action@github.com"
          git add .
          git diff --quiet && git diff --staged --quiet || (git commit -m "chore: update dataset" && git push)
```

### Script Modification Requirements

The `scripts/update_dataset.py` (or equivalent) MUST:
1. Use `kaggle.api.dataset_download_files` to fetch the data.
2. Implement idempotent logic: compare checksums or metadata before processing files.
3. Not rely on intermediate temporary files; update directly into the target directory.
4. Exit gracefully if no changes are required.
