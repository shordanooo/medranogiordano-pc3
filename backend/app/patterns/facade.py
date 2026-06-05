"""
Patron Facade: VozCiudadanaFacade provee una interfaz unificada
a los subsistemas de propuestas, firmas y envío al Congreso.
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import Proposal, Signature, ProposalStatus
from app.patterns.composite import LegislativeDocument
from app.patterns.decorator import BaseProposalOperation, build_signature_validator
from app.services.crypto_service import CryptoService
from app.services.congress_service import CongressService

MAX_SIGNATURES = 25_000
MAX_DAYS = 90


class VozCiudadanaFacade:
    """
    Fachada principal del sistema. Coordina: creación de propuestas,
    recolección de firmas, congelamiento criptográfico y envío al Congreso.
    """

    def __init__(self, db: Session):
        self.db = db
        self.crypto = CryptoService()
        self.congress = CongressService()

    def create_proposal(self, title: str, summary: str, full_text: str, author_id: int) -> Proposal:
        deadline = datetime.utcnow() + timedelta(days=MAX_DAYS)
        proposal = Proposal(
            title=title,
            summary=summary,
            full_text=full_text,
            author_id=author_id,
            deadline=deadline,
            status=ProposalStatus.COLLECTING,
        )
        self.db.add(proposal)
        self.db.commit()
        self.db.refresh(proposal)
        return proposal

    def sign_proposal(self, proposal_id: int, citizen_id: int, ip_address: str) -> dict:
        proposal = self.db.query(Proposal).filter(Proposal.id == proposal_id).first()
        if not proposal:
            return {"success": False, "error": "Propuesta no encontrada."}

        existing_ids = [s.citizen_id for s in proposal.signatures if s.is_valid]
        validation_data = {
            "deadline": proposal.deadline,
            "signature_count": proposal.signature_count,
            "existing_signers": existing_ids,
            "citizen_id": citizen_id,
            "status": proposal.status.value,
        }

        validator = build_signature_validator(BaseProposalOperation())
        result = validator.execute(validation_data)
        if not result["success"]:
            return result

        signature = Signature(
            proposal_id=proposal_id,
            citizen_id=citizen_id,
            ip_address=ip_address,
            is_valid=True,
        )
        self.db.add(signature)
        proposal.signature_count += 1
        self.db.commit()

        if proposal.signature_count >= MAX_SIGNATURES:
            return self._freeze_and_submit(proposal)

        return {"success": True, "signature_count": proposal.signature_count}

    def _freeze_and_submit(self, proposal: Proposal) -> dict:
        doc = (
            LegislativeDocument(proposal.id, proposal.title)
            .add_section("resumen", proposal.summary)
            .add_section("texto_completo", proposal.full_text)
            .add_signatures_section(proposal.signature_count)
            .build()
        )

        crypto_hash = self.crypto.freeze_document(doc)
        ticket = self.congress.submit(proposal.id, doc, crypto_hash)

        proposal.status = ProposalStatus.FROZEN
        proposal.frozen_at = datetime.utcnow()
        proposal.crypto_hash = crypto_hash
        proposal.submitted_to_congress = True
        proposal.congress_ticket = ticket
        self.db.commit()
        self.db.refresh(proposal)

        return {
            "success": True,
            "message": "¡Propuesta alcanzó 25,000 firmas! Congelada y enviada al Congreso.",
            "crypto_hash": crypto_hash,
            "congress_ticket": ticket,
            "signature_count": proposal.signature_count,
        }

    def get_proposal_status(self, proposal_id: int) -> dict:
        proposal = self.db.query(Proposal).filter(Proposal.id == proposal_id).first()
        if not proposal:
            return {"error": "Propuesta no encontrada."}

        if proposal.status == ProposalStatus.COLLECTING and datetime.utcnow() > proposal.deadline:
            proposal.status = ProposalStatus.EXPIRED
            self.db.commit()

        days_remaining = max(0, (proposal.deadline - datetime.utcnow()).days)
        return {
            "id": proposal.id,
            "title": proposal.title,
            "status": proposal.status.value,
            "signature_count": proposal.signature_count,
            "signatures_needed": max(0, MAX_SIGNATURES - proposal.signature_count),
            "progress_percent": round((proposal.signature_count / MAX_SIGNATURES) * 100, 2),
            "days_remaining": days_remaining,
            "crypto_hash": proposal.crypto_hash,
            "congress_ticket": proposal.congress_ticket,
        }
