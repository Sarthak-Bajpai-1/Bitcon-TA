from dataclasses import dataclass
from datetime import datetime

@dataclass
class NetworkRecord:
    record_id: str
    timestamp: datetime
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
