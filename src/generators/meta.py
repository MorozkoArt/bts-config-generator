from typing import Dict, List
from ..models.class_info import ClassInfo


class MetaGenerator:
    def generate(self, classes: Dict[str, ClassInfo]) -> List[Dict]:
        return [self._process_class(cls) for cls in classes.values()]

    def _process_class(self, class_info: ClassInfo) -> Dict:
        entry = {
            "class": class_info.name,
            "documentation": class_info.documentation,
            "isRoot": class_info.is_root,
        }
        if not class_info.is_root:
            self._add_multiplicity(entry, class_info)
        entry["parameters"] =  self._process_parameters(class_info)

        return entry

    def _process_parameters(self, class_info: ClassInfo) -> List[Dict]:
        params = []
        params.extend({
                        "name": attr.name,
                        "type": attr.type
                    } for attr in class_info.attributes)
        params.extend({
                        "name": rel.source,
                        "type": "class"
                    } for rel in class_info.relations if rel.source)
        return params

    def _add_multiplicity(self, entry: Dict, class_info: ClassInfo):
        if class_info.relations:
            multiplicity = class_info.relations[0].source_multiplicity
            if ".." in multiplicity:
                min_val, max_val = multiplicity.split("..")
                entry["max"] = max_val.strip("]")
                entry["min"] = min_val.strip("[")
            else:
                entry["max"] = multiplicity
                entry["min"] = multiplicity
