import csv

def load_csv(file_path):
    """Load CSV rows as dictionaries; values remain raw strings."""
    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV file is empty or has no header.")
        return list(reader)
