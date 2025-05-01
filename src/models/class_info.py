from dataclasses import dataclass, field
from typing import List
from .attribute import Attribute
from .class_relation import ClassRelation

@dataclass
class ClassInfo:
    name: str
    is_root: bool
    documentation: str
    attributes: List[Attribute] = field(default_factory=list)
    relations: List[ClassRelation] = field(default_factory=list)