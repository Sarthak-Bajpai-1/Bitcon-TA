from dataclasses import dataclass

@dataclass
class Evidence:
    evidence_id: str
    source: str
    source_record_id: str
    evidence_type: str
    description: str
    confidence: float
