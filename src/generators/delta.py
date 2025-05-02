from typing import Dict, List, Any


class DeltaGenerator:
    def compare(self, original: Dict[str, Any], patched: Dict[str, Any]) -> Dict:
        return {
            "additions": self._find_additions(original, patched),
            "deletions": self._find_deletions(original, patched),
            "updates": self._find_updates(original, patched)
        }

    def apply(self, original: Dict[str, Any], delta: Dict) -> Dict[str, Any]:
        result = original.copy()
        for key in delta["deletions"]:
            result.pop(key, None)
        for update in delta["updates"]:
            result[update["key"]] = update["to"]
        for addition in delta["additions"]:
            result[addition["key"]] = addition["value"]
        return result

    def _find_additions(self, original: Dict, patched: Dict) -> List[Dict]:
        return [
            {"key": k, "value": v}
            for k, v in patched.items()
            if k not in original
        ]

    def _find_deletions(self, original: Dict, patched: Dict) -> List[str]:
        return [k for k in original if k not in patched]

    def _find_updates(self, original: Dict, patched: Dict) -> List[Dict]:
        return [
            {"key": k, "from": original[k], "to": v}
            for k, v in patched.items()
            if k in original and original[k] != v
        ]