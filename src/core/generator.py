import os
from typing import Dict, Any, Tuple
from ..parsers.xml_parser import XmlModelParser
from ..generators.config import ConfigGenerator
from ..generators.meta import MetaGenerator
from ..generators.delta import DeltaGenerator
from ..utils.file_io import read_json, write_json, write_file


class BTSConfigGenerator:
    def __init__(self):
        self.parser = XmlModelParser()
        self.config_gen = ConfigGenerator()
        self.meta_gen = MetaGenerator()
        self.delta_gen = DeltaGenerator()

    def generate_artifacts(self):
        classes = self._parse_model()
        original_config, patched_config = self._load_configs()
        self._generate_outputs(classes, original_config, patched_config)

    def _parse_model(self) -> Dict[str, Any]:
        xml_path = "input/impulse_test_input.xml"
        if not os.path.exists(xml_path):
            raise FileNotFoundError(f"XML model file missing: {xml_path}")
        return self.parser.parse(xml_path)

    def _load_configs(self) -> Tuple[Dict, Dict]:
        config_path = "input/config.json"
        patched_path = "input/patched_config.json"

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file missing: {config_path}")
        if not os.path.exists(patched_path):
            raise FileNotFoundError(f"Patched config file missing: {patched_path}")

        return read_json(config_path), read_json(patched_path)

    def _generate_outputs(self, classes: Dict, original: Dict, patched: Dict):
        write_file("out/config.xml", self.config_gen.generate(classes))
        write_json("out/meta.json", self.meta_gen.generate(classes))

        delta = self.delta_gen.compare(original, patched)
        write_json("out/delta.json", delta)

        result = self.delta_gen.apply(original, delta)
        write_json("out/res_patched_config.json", result)