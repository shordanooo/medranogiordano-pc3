import hashlib
import json
from datetime import datetime


class CryptoService:
    """Servicio de congelamiento criptográfico del documento legislativo."""

    def freeze_document(self, document: dict) -> str:
        payload = json.dumps(document, sort_keys=True, default=str)
        timestamp = datetime.utcnow().isoformat()
        combined = f"{payload}|{timestamp}"
        return hashlib.sha512(combined.encode("utf-8")).hexdigest()

    def verify_document(self, document: dict, stored_hash: str) -> bool:
        current_hash = hashlib.sha512(
            json.dumps(document, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()
        return current_hash == stored_hash
