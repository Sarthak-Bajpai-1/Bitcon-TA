import unittest
from datetime import datetime

from backend.app.ingestion.validator import validate_network_record
from backend.app.ingestion.normalizer import normalize_network_record

VALID = {
    "timestamp": "2026-09-30T10:30:00+05:30",
    "src_ip": "192.168.1.10",
    "dst_ip": "192.168.1.20",
    "src_port": "49152",
    "dst_port": "8333",
}

class PipelineTests(unittest.TestCase):
    def test_valid_record_passes(self):
        self.assertEqual(validate_network_record(VALID), [])

    def test_bad_ip_fails(self):
        row = dict(VALID, src_ip="not-an-ip")
        self.assertIn("Invalid source IP", validate_network_record(row))

    def test_bad_port_fails(self):
        row = dict(VALID, src_port="abc")
        self.assertIn("Source port is not an integer", validate_network_record(row))

    def test_port_out_of_range_fails(self):
        row = dict(VALID, dst_port="70000")
        self.assertTrue(any("between 0 and 65535" in e for e in validate_network_record(row)))

    def test_timezone_required(self):
        row = dict(VALID, timestamp="2026-09-30T10:30:00")
        self.assertIn("Timestamp must include a timezone offset", validate_network_record(row))

    def test_normalization_converts_types(self):
        result = normalize_network_record(VALID, "NET-000001")
        self.assertEqual(result.src_port, 49152)
        self.assertEqual(result.dst_port, 8333)
        self.assertIsInstance(result.timestamp, datetime)
        self.assertIsNotNone(result.timestamp.utcoffset())
        self.assertEqual(result.record_id, "NET-000001")

if __name__ == "__main__":
    unittest.main()
