"""
Patron Decorator: Añade capas de validación a las operaciones
sobre propuestas legislativas sin modificar la clase base.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class ProposalOperation(ABC):
    """Interfaz base para operaciones sobre propuestas."""

    @abstractmethod
    def execute(self, data: dict) -> dict:
        pass


class BaseProposalOperation(ProposalOperation):
    """Operación básica sin validaciones adicionales."""

    def execute(self, data: dict) -> dict:
        return {"success": True, "data": data}


class ProposalDecorator(ProposalOperation):
    """Decorador base que envuelve una operación."""

    def __init__(self, wrapped: ProposalOperation):
        self._wrapped = wrapped

    def execute(self, data: dict) -> dict:
        return self._wrapped.execute(data)


class DeadlineValidatorDecorator(ProposalDecorator):
    """Valida que la propuesta no haya expirado."""

    def execute(self, data: dict) -> dict:
        deadline: Optional[datetime] = data.get("deadline")
        if deadline and datetime.utcnow() > deadline:
            return {
                "success": False,
                "error": "La propuesta ha expirado. El plazo de 90 días ha vencido.",
            }
        return super().execute(data)


class SignatureLimitDecorator(ProposalDecorator):
    """Valida que no se exceda el límite de 25,000 firmas."""

    MAX_SIGNATURES = 25_000

    def execute(self, data: dict) -> dict:
        count: int = data.get("signature_count", 0)
        if count >= self.MAX_SIGNATURES:
            return {
                "success": False,
                "error": "La propuesta ya alcanzó el límite de 25,000 firmas.",
            }
        return super().execute(data)


class DuplicateSignatureDecorator(ProposalDecorator):
    """Valida que el ciudadano no haya firmado ya la propuesta."""

    def execute(self, data: dict) -> dict:
        existing_signers: list = data.get("existing_signers", [])
        citizen_id: int = data.get("citizen_id", -1)
        if citizen_id in existing_signers:
            return {
                "success": False,
                "error": "Ya firmaste esta propuesta. Solo se permite una firma por ciudadano.",
            }
        return super().execute(data)


class StatusValidatorDecorator(ProposalDecorator):
    """Valida que la propuesta esté en estado COLLECTING."""

    def execute(self, data: dict) -> dict:
        status: str = data.get("status", "")
        if status != "collecting":
            return {
                "success": False,
                "error": f"No se puede firmar una propuesta con estado '{status}'.",
            }
        return super().execute(data)


def build_signature_validator(operation: ProposalOperation) -> ProposalOperation:
    """Compone todos los decoradores de validación para firma."""
    return (
        DeadlineValidatorDecorator(
            SignatureLimitDecorator(
                DuplicateSignatureDecorator(
                    StatusValidatorDecorator(operation)
                )
            )
        )
    )
