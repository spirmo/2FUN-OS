import json
import os


class RuleRegistry:
    """Cached JSON rule loader preserving the Legacy contract."""

    def __init__(self):
        self.cache = {}
        self.timestamps = {}

    def load_rule_file(self, path):
        modified = os.path.getmtime(path)

        if path not in self.timestamps or self.timestamps[path] != modified:
            with open(path, "r", encoding="utf-8") as file:
                self.cache[path] = json.load(file)

            self.timestamps[path] = modified

        return self.cache[path]
