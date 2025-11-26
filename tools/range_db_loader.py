import json
from pathlib import Path

def load_ranges(path=None):
    if path is None:
        path = Path(__file__).resolve().parents[1] / 'medical_ranges.json'
    with open(path) as f:
        return json.load(f)