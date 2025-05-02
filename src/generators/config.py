from typing import Dict
from ..models.class_info import ClassInfo


class ConfigGenerator:
    def generate(self, classes: Dict[str, ClassInfo]) -> str:
        root_class = next((c for c in classes.values() if c.is_root), None)
        if not root_class:
            return "<?xml version=\"1.0\" ?>\n<error>No root class found</error>"

        return self._build_xml(root_class, classes)

    def _build_xml(self, class_info: ClassInfo, classes: Dict[str, ClassInfo], indent: int = 0) -> str:
        indent_str = "    " * indent
        xml = f"{indent_str}<{class_info.name}>\n"

        for attr in class_info.attributes:
            xml += f"{indent_str}    <{attr.name}>{attr.type}</{attr.name}>\n"

        for rel in class_info.relations:
            if rel.source in classes:
                xml += self._build_xml(classes[rel.source], classes, indent + 1)

        xml += f"{indent_str}</{class_info.name}>\n"
        return xml