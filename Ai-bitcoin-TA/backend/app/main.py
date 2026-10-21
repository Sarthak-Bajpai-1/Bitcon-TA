from pathlib import Path

from backend.app.ingestion.csv_loader import load_csv
from backend.app.ingestion.validator import validate_network_record
from backend.app.ingestion.normalizer import normalize_network_record
from backend.app.models.evidence import Evidence

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "network.csv"

def main():
    records = load_csv(CSV_PATH)
    valid_count = 0
    invalid_count = 0

    print(f"Input file: {CSV_PATH}")
    print(f"Rows loaded: {len(records)}\n")

    for index, record in enumerate(records, start=1):
        errors = validate_network_record(record)

        if errors:
            invalid_count += 1
            print(f"Invalid record (row {index}):")
            for error in errors:
                print(f" - {error}")
            print()
            continue

        normalized = normalize_network_record(record, f"NET-{index:06d}")
        evidence = Evidence(
            evidence_id=f"EVD-{index:06d}",
            source="network.csv",
            source_record_id=normalized.record_id,
            evidence_type="OBSERVED",
            description=f"{normalized.src_ip} communicated with {normalized.dst_ip}",
            confidence=1.0,
        )

        valid_count += 1
        print("Valid normalized record:")
        print(normalized)
        print("Evidence:")
        print(evidence)
        print("-" * 72)

    print(f"\nSummary: {valid_count} valid row(s), {invalid_count} invalid row(s).")

if __name__ == "__main__":
    main()
