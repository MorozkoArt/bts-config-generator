from dataclasses import dataclass

@dataclass
class ClassRelation:
    source_multiplicity: str
    target_multiplicity: str
    source: str = ""
    target: str = ""