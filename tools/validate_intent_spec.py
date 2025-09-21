#!/usr/bin/env python3
"""Validator mínimo para archivos intent-spec (formato JSON).

Uso:
    python3 tools/validate_intent_spec.py path/to/spec.json

El objetivo es comprobar que existen las secciones esperadas y que las
listas obligatorias contienen elementos. Para validación completa, usar
jsonschema con `docs/specs/intent_spec.schema.json`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_TOP_LEVEL = ("identity", "intent", "contracts", "validation")

REQUIRED_IDENTITY = ("id", "name", "version", "hash")
REQUIRED_INTENT = ("prompt_signature", "requirements")
REQUIRED_CONTRACTS = ("input_schema", "output_schema")
REQUIRED_VALIDATION = ("required_tests", "rollback_strategy")


class ValidationError(Exception):
    pass


def _ensure_keys(data: Dict[str, Any], keys: tuple[str, ...], prefix: str) -> None:
    missing = [key for key in keys if key not in data]
    if missing:
        raise ValidationError(f"Faltan claves {missing} en {prefix}")


def _ensure_non_empty_sequence(data: Dict[str, Any], key: str, prefix: str) -> None:
    value = data.get(key, [])
    if not isinstance(value, list) or not value:
        raise ValidationError(f"{prefix}.{key} debe ser una lista no vacía")


def validate(spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    try:
        _ensure_keys(spec, REQUIRED_TOP_LEVEL, "root")
        _ensure_keys(spec["identity"], REQUIRED_IDENTITY, "identity")
        _ensure_keys(spec["intent"], REQUIRED_INTENT, "intent")
        _ensure_non_empty_sequence(spec["intent"], "requirements", "intent")
        _ensure_keys(spec["contracts"], REQUIRED_CONTRACTS, "contracts")
        _ensure_keys(spec["validation"], REQUIRED_VALIDATION, "validation")
        _ensure_non_empty_sequence(spec["validation"], "required_tests", "validation")
    except ValidationError as exc:
        errors.append(str(exc))

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python3 tools/validate_intent_spec.py <archivo.json>", file=sys.stderr)
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Archivo no encontrado: {path}", file=sys.stderr)
        return 1

    spec = json.loads(path.read_text())
    errors = validate(spec)

    if errors:
        print("intent-spec inválido:")
        for err in errors:
            print(f" - {err}")
        return 1

    print("intent-spec válido ✔")
    return 0


if __name__ == "__main__":
    sys.exit(main())
