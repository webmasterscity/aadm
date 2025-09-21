"""Atom: validate email against RFC-like regex.

Pequeño propósito: comprobar formato y devolver resultado estructurado.
"""
import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_email(email: str) -> dict:
    """Valida el correo y describe el resultado.

    Retorna estructura con `valid` boolean y `error` opcional para
    facilitar composición declarativa.
    """

    valid = bool(EMAIL_PATTERN.match(email))
    return {"valid": valid, "error": None if valid else "Invalid format"}
