import pandas as pd
import os
from datetime import datetime
import re
from glob import glob

from settings import settings


def parse_date_from_log(file_path: str) -> str | None:
    """Parse date from Zoom log file (fixed format)"""
    date_regex = r'(?:"|\b)([A-Za-z]{3} \d{1,2},? \d{4})\b'
    date_format = "%b %d %Y"

    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            for line in f:
                date_match = re.search(date_regex, line)
                if date_match:
                    date_str = date_match.group(1).replace(",", "").strip()
                    return datetime.strptime(date_str, date_format).strftime("%d.%m.%Y")
        print(f"Date not found: {os.path.basename(file_path)}")
        return None
    except Exception as e:
        print(f"Error: {os.path.basename(file_path)} - {str(e)}")
        return None


def process_files():
    """Main processing function for Zoom logs"""
    all_data = {}
    os.makedirs(settings.output_dir, exist_ok=True)

    # Get all CSV files in input directory
    csv_files = glob(os.path.join(settings.input_dir, "*.csv"))
    if not csv_files:
        print(f"No CSV files found in: {settings.input_dir}")
        return

    for file_path in csv_files:
        date = parse_date_from_log(file_path)
        if not date:
            continue

        try:
            # Read and process participant data
            df = pd.read_csv(
                file_path,
                skiprows=3,
                usecols=[0],
                header=None,
                names=["name"],
                dtype={"name": str},
                encoding="utf-8-sig",
            )

            # Clean and normalize participant names
            participants = set(
                df["name"]
                .str.replace(r"\s*\(Guest\).*", "", regex=True)
                .str.strip(' "()')
                .replace("", pd.NA)
                .dropna()
                .unique()
            )

            all_data[date] = participants

        except Exception as e:
            print(f"Error processing {os.path.basename(file_path)}: {str(e)}")
            continue

    # Sort dates chronologically
    all_dates_sorted = sorted(
        all_data.keys(), key=lambda x: datetime.strptime(x, "%d.%m.%Y")
    )

    # Create attendance matrix
    all_names = sorted({name for names in all_data.values() for name in names})
    report = pd.DataFrame(
        index=all_names,
        columns=all_dates_sorted,
        data=[
            [1 if name in all_data[date] else 0 for date in all_dates_sorted]
            for name in all_names
        ],
    )

    # Save CSV report
    csv_path = os.path.join(settings.output_dir, settings.output_csv_file)
    report.reset_index().rename(columns={"index": "Name"}).to_csv(
        csv_path, index=False, encoding="utf-8-sig"
    )

    # Save Excel report
    xlsx_path = os.path.join(settings.output_dir, settings.output_xlsx_file)
    report.reset_index().rename(columns={"index": "Name"}).to_excel(
        xlsx_path, index=False, engine="openpyxl"
    )

    print(f"Reports saved:\n- CSV: {csv_path}\n- XLSX: {xlsx_path}")


if __name__ == "__main__":
    process_files()