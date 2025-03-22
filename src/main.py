import pandas as pd
import os
from datetime import datetime
import re
from glob import glob

from settings import settings


def parse_date_from_log(file_path: str) -> str | None:
    """Парсинг даты из лог-файла (фиксированные настройки)"""
    date_regex = r'(?:"|\b)([A-Za-z]{3} \d{1,2},? \d{4})\b'
    date_format = "%b %d %Y"

    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            for line in f:
                date_match = re.search(date_regex, line)
                if date_match:
                    date_str = date_match.group(1).replace(",", "").strip()
                    return datetime.strptime(date_str, date_format).strftime("%d.%m.%Y")
        print(f"Дата не найдена: {os.path.basename(file_path)}")
        return None
    except Exception as e:
        print(f"Ошибка: {os.path.basename(file_path)} - {str(e)}")
        return None


def process_files():
    all_data = {}
    os.makedirs(settings.output_dir, exist_ok=True)

    # Получаем все CSV-файлы в директории
    csv_files = glob(os.path.join(settings.input_dir, "*.csv"))
    if not csv_files:
        print(f"Нет CSV-файлов в: {settings.input_dir}")
        return

    for file_path in csv_files:
        date = parse_date_from_log(file_path)
        if not date:
            continue

        try:
            df = pd.read_csv(
                file_path,
                skiprows=3,
                usecols=[0],
                header=None,
                names=["name"],
                dtype={"name": str},
                encoding="utf-8-sig",
            )

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
            print(f"Ошибка обработки {os.path.basename(file_path)}: {str(e)}")
            continue

    # Сортировка и формирование отчета
    all_dates_sorted = sorted(
        all_data.keys(), key=lambda x: datetime.strptime(x, "%d.%m.%Y")
    )

    all_names = sorted({name for names in all_data.values() for name in names})
    report = pd.DataFrame(
        index=all_names,
        columns=all_dates_sorted,
        data=[
            [1 if name in all_data[date] else 0 for date in all_dates_sorted]
            for name in all_names
        ],
    )

    # Сохранение
    output_path = os.path.join(settings.output_dir, settings.output_file)
    report.reset_index().rename(columns={"index": "Имя"}).to_csv(
        output_path, index=False, encoding="utf-8-sig"
    )


if __name__ == "__main__":
    process_files()
    print(f"Отчет сохранен: {os.path.join(settings.output_dir, settings.output_file)}")
