import ipaddress
from datetime import datetime

REQUIRED_FIELDS = ("timestamp", "src_ip", "dst_ip", "src_port", "dst_port")

def validate_network_record(record):
    """Return a list of validation errors; an empty list means valid."""
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in record or record[field] is None or str(record[field]).strip() == "":
            errors.append(f"Missing or empty field: {field}")

    if errors:
        return errors

    for field, label in (("src_ip", "source"), ("dst_ip", "destination")):
        try:
            ipaddress.ip_address(record[field].strip())
        except ValueError:
            errors.append(f"Invalid {label} IP")

    for field, label in (("src_port", "Source"), ("dst_port", "Destination")):
        try:
            port = int(record[field])
            if not 0 <= port <= 65535:
                errors.append(f"Invalid {label.lower()} port: must be between 0 and 65535")
        except (ValueError, TypeError):
            errors.append(f"{label} port is not an integer")

    try:
        parsed_timestamp = datetime.fromisoformat(record["timestamp"].strip())
        if parsed_timestamp.tzinfo is None or parsed_timestamp.utcoffset() is None:
            errors.append("Timestamp must include a timezone offset")
    except (ValueError, TypeError):
        errors.append("Timestamp is not a valid ISO-8601 datetime")

    return errors
