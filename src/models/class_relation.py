from dataclasses import dataclass

@dataclass
class ClassRelation:
    target: str
    source: str
    source_multiplicity: str
    target_multiplicity: str