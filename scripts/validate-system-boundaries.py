#!/usr/bin/env python3
"""Validate integration and real-world-validation registry truth boundaries."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_json(path: Path):
    require(path.is_file(), f"missing required file: {path}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_integrations(root: Path) -> None:
    data = load_json(root / "integrations" / "registry.json")
    require(data.get("version") == 1, "integration registry version must be 1")
    adapters = data.get("adapters")
    require(isinstance(adapters, list) and adapters, "integration registry must contain adapters")
    ids = set()
    required = {
        "id", "provider", "capability", "status", "authentication",
        "minimum_permissions", "secrets_rule", "supported_objects",
        "read_boundary", "write_boundary", "verification", "rollback",
        "freshness", "notes",
    }
    allowed_status = {"contract-defined", "configured", "authenticated", "connected", "authorized", "verified"}
    for adapter in adapters:
        require(isinstance(adapter, dict), "integration adapter must be an object")
        missing = required - set(adapter)
        require(not missing, f"integration adapter missing fields: {sorted(missing)}")
        identifier = adapter["id"]
        require(isinstance(identifier, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]*", identifier), f"invalid adapter id: {identifier!r}")
        require(identifier not in ids, f"duplicate adapter id: {identifier}")
        ids.add(identifier)
        require(adapter["status"] in allowed_status, f"{identifier}: invalid status")
        require(adapter["status"] == "contract-defined", f"{identifier}: repository must not claim user/runtime live state")
        for field in ("minimum_permissions", "supported_objects"):
            require(isinstance(adapter[field], list) and adapter[field] and all(isinstance(x, str) and x.strip() for x in adapter[field]), f"{identifier}: {field} must be nonempty strings")
        require("never repository" in adapter["secrets_rule"].lower(), f"{identifier}: secrets must be excluded from repository")


def governed_skills(root: Path) -> set[str]:
    skill_root = root / ".agents" / "skills"
    return {p.parent.name for p in skill_root.glob("*/SKILL.md") if p.is_file()}


def validate_validation_registry(root: Path) -> None:
    data = load_json(root / "validation" / "registry.json")
    require(data.get("version") == 1, "validation registry version must be 1")
    records = data.get("records")
    require(isinstance(records, list), "validation records must be a list")
    skills = governed_skills(root)
    ids = set()
    classes = {"synthetic", "anonymized-real", "verified-public"}
    states = {"registered", "evidence-complete", "implementation-verified", "outcome-mature", "reviewed", "publishable"}
    for record in records:
        require(isinstance(record, dict), "validation record must be an object")
        for field in ("id", "owner", "evidence_class", "state", "publication", "provenance", "limitations"):
            require(field in record, f"validation record missing {field}")
        identifier = record["id"]
        require(isinstance(identifier, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]*", identifier), f"invalid validation id: {identifier!r}")
        require(identifier not in ids, f"duplicate validation id: {identifier}")
        ids.add(identifier)
        require(record["owner"] in skills, f"{identifier}: owner is not a governed skill")
        require(record["evidence_class"] in classes, f"{identifier}: invalid evidence class")
        require(record["state"] in states, f"{identifier}: invalid validation state")
        require(isinstance(record["provenance"], str) and record["provenance"].strip(), f"{identifier}: provenance required")
        require(isinstance(record["limitations"], str) and record["limitations"].strip(), f"{identifier}: limitations required")
        if record["evidence_class"] != "verified-public":
            require(record["publication"] != "public-case-study", f"{identifier}: only verified-public evidence may be a public case study")
        if record["state"] == "publishable":
            require(record["evidence_class"] == "verified-public", f"{identifier}: publishable requires verified-public evidence")
            require(record["publication"] == "public-case-study", f"{identifier}: publishable state requires public-case-study publication status")


def validate_analytics_owner(root: Path) -> None:
    skills = governed_skills(root)
    require("marketing-analytics" in skills, "marketing-analytics governed skill is missing")
    registry = (root / "CAPABILITY-REGISTRY.md").read_text(encoding="utf-8")
    require("$marketing-analytics" in registry, "capability registry does not route analytics engineering to $marketing-analytics")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        validate_integrations(root)
        validate_validation_registry(root)
        validate_analytics_owner(root)
    except (ValidationError, json.JSONDecodeError, OSError) as error:
        print(f"System-boundary validation failed: {error}", file=sys.stderr)
        return 1
    print("System boundary contracts valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
