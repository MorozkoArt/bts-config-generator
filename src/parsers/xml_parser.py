import xml.etree.ElementTree as ET
from typing import Dict
from ..models.class_info import ClassInfo
from ..models.attribute import Attribute
from ..models.class_relation import ClassRelation


class XmlModelParser:
    def __init__(self):
        self.classes: Dict[str, ClassInfo] = {}

    def parse(self, xml_file: str) -> Dict[str, ClassInfo]:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for elem in root:
            if elem.tag == "Class":
                self._parse_class(elem)

        for elem in root:
            if elem.tag == "Aggregation":
                self._parse_aggregation(elem)

        return self.classes

    def _parse_class(self, elem: ET.Element):
        class_info = ClassInfo(
            name=elem.attrib["name"],
            is_root=elem.attrib["isRoot"] == "true",
            documentation=elem.attrib.get("documentation", "")
        )

        for attr in elem.findall("Attribute"):
            class_info.attributes.append(
                Attribute(name=attr.attrib["name"], type=attr.attrib["type"])
            )

        self.classes[class_info.name] = class_info

    def _parse_aggregation(self, elem: ET.Element):
        relation = ClassRelation(
            target=elem.attrib["target"],
            source=elem.attrib["source"],
            source_multiplicity=elem.attrib["sourceMultiplicity"],
            target_multiplicity=elem.attrib["targetMultiplicity"]
        )

        if relation.target in self.classes:
            self.classes[relation.target].relations.append(relation)