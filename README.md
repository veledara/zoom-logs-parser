# zoom-logs-parser

## Description

A script for analyzing Zoom conference logs and generating an attendance summary report. 

Key features:
- Automatically detects lecture/meeting dates from log contents
- Extracts a list of all participants from a set of CSV files
- Generates a participation matrix report in .csv and .xlsx formats:
    - Rows: unique participant names
    - Columns: lecture/meeting dates
    - Values: 1 (attended) or 0 (absent)

Can be used to simplify filling out online lecture attendance tables.

![Final Report](https://github.com/user-attachments/assets/ee5437f4-f14b-4299-8b90-261bb5fb9a33)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/veledara/zoom-logs-parser.git

cd zoom-logs-parser
```

2. Install [poetry](https://python-poetry.org/docs/#installation) (if not installed)

3. Install dependencies:
```bash
poetry install
```
4. Create environment file:
```bash
cp .env.example .env
```

## Environment Configuration
Edit the `.env` file according to your needs:

```ini
input_dir=logs                     # Directory containing source CSV files
output_dir=output                  # Directory for report output
output_csv_file=full_report.csv    # Output CSV filename
output_xlsx_file=full_report.xlsx  # Output Excel filename
```

## Usage
Place Zoom CSV logs in the configured input directory (default: `logs/`)

Run the script:
```bash
poetry run python src/main.py
```
or

```bash
python src/main.py
```

Generated reports will be saved in the specified output directory.
