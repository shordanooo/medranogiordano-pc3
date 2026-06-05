import uuid
from datetime import datetime


class CongressService:
    """Simula el envío de propuestas a la Oficina del Congreso."""

    def submit(self, proposal_id: int, document: dict, crypto_hash: str) -> str:
        ticket = f"CONGRESO-{proposal_id}-{uuid.uuid4().hex[:8].upper()}"
        print(f"[CongressService] Propuesta {proposal_id} enviada. Ticket: {ticket}")
        return ticket
