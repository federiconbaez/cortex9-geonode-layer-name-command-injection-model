"""Fixture loading shared by tests and scripts/gen_results.py."""
from __future__ import annotations

import json
from pathlib import Path

from . import ogr

ROOT = Path(__file__).resolve().parents[2]


def load() -> list:
    data = (ROOT / "fixtures/cases.json").read_text(encoding="utf-8")
    return json.loads(data)["cases"]


def run(case: dict, version: str) -> dict:
    return ogr.analyze(version, case["input_file"], case["alternate"],
                       case["original_name"])
