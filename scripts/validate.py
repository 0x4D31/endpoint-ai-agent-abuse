#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / "data" / "catalog.json").read_text())

ids = [t["id"] for t in catalog["techniques"]]
if len(ids) != len(set(ids)):
    raise SystemExit("duplicate technique id")

surfaces = set(catalog["surfaces"])
unknown = sorted({t["surface"] for t in catalog["techniques"]} - surfaces)
if unknown:
    raise SystemExit(f"unknown surfaces: {', '.join(unknown)}")

print(f"ok: {len(catalog['techniques'])} techniques, {len(catalog.get('candidates', []))} candidates")
