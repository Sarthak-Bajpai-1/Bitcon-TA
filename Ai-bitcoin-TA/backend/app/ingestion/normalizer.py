from datetime import datetime
from backend.app.models.records import NetworkRecord

def normalize_network_record(record, record_id):
    """Convert a validated raw CSV row into a typed NetworkRecord."""
    timestamp = datetime.fromisoformat(record["timestamp"].strip())
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("Timestamp must be timezone-aware")

    return NetworkRecord(
        record_id=record_id,
        timestamp=timestamp,
        src_ip=record["src_ip"].strip(),
        dst_ip=record["dst_ip"].strip(),
        src_port=int(record["src_port"]),
        dst_port=int(record["dst_port"]),
    )
