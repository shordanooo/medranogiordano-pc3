"""
Casos de Prueba - Plataforma Voz del Ciudadano
CP-01: Creación exitosa de propuesta legislativa
CP-02: Firma que alcanza el límite de 25,000 activa congelamiento
CP-03: Firma rechazada por propuesta expirada
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from app.patterns.decorator import (
    BaseProposalOperation,
    build_signature_validator,
    DeadlineValidatorDecorator,
    SignatureLimitDecorator,
    DuplicateSignatureDecorator,
    StatusValidatorDecorator,
)
from app.patterns.composite import LegislativeDocument
from app.patterns.facade import VozCiudadanaFacade, MAX_SIGNATURES


# ─── CP-01: Creación exitosa de propuesta ───────────────────────────────────

class TestCP01_CreacionPropuesta:
    """CP-01: Un colectivo civil crea una propuesta legislativa válida."""

    def test_composite_construye_documento_completo(self):
        """El patrón Composite genera el documento con todas las secciones."""
        doc = (
            LegislativeDocument(1, "Ley de Transparencia Digital")
            .add_section("resumen", "Propuesta para garantizar transparencia en datos públicos.")
            .add_section("texto_completo", "Artículo 1: El Estado garantiza acceso a datos...")
            .add_signatures_section(0)
            .build()
        )
        assert doc["proposal_id"] == 1
        assert doc["total_words"] > 0
        content = doc["content"]
        assert content["section"] == "documento_legislativo"
        assert len(content["children"]) == 4

    def test_facade_crea_propuesta_con_deadline_90_dias(self):
        """La fachada asigna un plazo de exactamente 90 días."""
        db_mock = MagicMock()
        facade = VozCiudadanaFacade(db_mock)

        captured = {}

        def fake_add(obj):
            captured["proposal"] = obj

        db_mock.add.side_effect = fake_add
        db_mock.commit.return_value = None
        db_mock.refresh.return_value = None

        before = datetime.utcnow()
        facade.create_proposal("Ley de Agua Potable", "Resumen", "Texto completo", author_id=1)
        after = datetime.utcnow()

        proposal = captured["proposal"]
        delta = proposal.deadline - before
        assert timedelta(days=89) < delta <= timedelta(days=90) + (after - before)

    def test_propuesta_inicia_en_estado_collecting(self):
        """Una propuesta nueva debe iniciar en estado COLLECTING."""
        from app.models.models import ProposalStatus
        db_mock = MagicMock()
        facade = VozCiudadanaFacade(db_mock)
        captured = {}
        db_mock.add.side_effect = lambda obj: captured.update({"p": obj})
        db_mock.commit.return_value = None
        db_mock.refresh.return_value = None
        facade.create_proposal("Ley Test", "Resumen", "Texto", author_id=5)
        assert captured["p"].status.value == "collecting"


# ─── CP-02: Firma alcanza 25,000 → congelamiento automático ─────────────────

class TestCP02_CongelamientoAutomatico:
    """CP-02: Al llegar a 25,000 firmas el sistema congela y envía al Congreso."""

    def test_limite_firma_rechaza_nueva_firma(self):
        """El decorador SignatureLimit bloquea firmas cuando ya hay 25,000."""
        op = build_signature_validator(BaseProposalOperation())
        data = {
            "deadline": datetime.utcnow() + timedelta(days=30),
            "signature_count": MAX_SIGNATURES,
            "existing_signers": [],
            "citizen_id": 99,
            "status": "collecting",
        }
        result = op.execute(data)
        assert result["success"] is False
        assert "25,000" in result["error"]

    def test_firma_numero_25000_activa_congelamiento(self):
        """La firma número 25,000 dispara el proceso de congelamiento."""
        from app.models.models import ProposalStatus, Proposal

        proposal_mock = MagicMock(spec=Proposal)
        proposal_mock.id = 1
        proposal_mock.title = "Ley de Educación Pública"
        proposal_mock.summary = "Resumen"
        proposal_mock.full_text = "Texto completo"
        proposal_mock.status = ProposalStatus.COLLECTING
        proposal_mock.signature_count = MAX_SIGNATURES - 1
        proposal_mock.deadline = datetime.utcnow() + timedelta(days=10)
        proposal_mock.signatures = []

        db_mock = MagicMock()
        db_mock.query.return_value.filter.return_value.first.return_value = proposal_mock

        facade = VozCiudadanaFacade(db_mock)
        result = facade.sign_proposal(1, citizen_id=42, ip_address="127.0.0.1")

        assert result["success"] is True
        assert "25,000" in result["message"]
        assert "crypto_hash" in result
        assert result["congress_ticket"].startswith("CONGRESO-")

    def test_hash_criptografico_es_sha512(self):
        """El hash generado debe ser SHA-512 (128 caracteres hexadecimales)."""
        from app.services.crypto_service import CryptoService
        svc = CryptoService()
        doc = {"proposal_id": 1, "content": "test"}
        h = svc.freeze_document(doc)
        assert len(h) == 128
        assert all(c in "0123456789abcdef" for c in h)


# ─── CP-03: Firma rechazada por propuesta expirada ──────────────────────────

class TestCP03_PropuestaExpirada:
    """CP-03: No se puede firmar una propuesta cuyo plazo de 90 días venció."""

    def test_decorador_rechaza_propuesta_expirada(self):
        """DeadlineValidator bloquea firmas cuando el deadline ya pasó."""
        op = build_signature_validator(BaseProposalOperation())
        data = {
            "deadline": datetime.utcnow() - timedelta(days=1),
            "signature_count": 5000,
            "existing_signers": [],
            "citizen_id": 10,
            "status": "collecting",
        }
        result = op.execute(data)
        assert result["success"] is False
        assert "expirado" in result["error"].lower() or "90" in result["error"]

    def test_facade_cambia_estado_a_expired(self):
        """La fachada detecta el vencimiento y actualiza el estado."""
        from app.models.models import ProposalStatus, Proposal

        proposal_mock = MagicMock(spec=Proposal)
        proposal_mock.id = 2
        proposal_mock.title = "Ley Expirada"
        proposal_mock.status = ProposalStatus.COLLECTING
        proposal_mock.signature_count = 1000
        proposal_mock.deadline = datetime.utcnow() - timedelta(days=91)
        proposal_mock.crypto_hash = None
        proposal_mock.congress_ticket = None

        db_mock = MagicMock()
        db_mock.query.return_value.filter.return_value.first.return_value = proposal_mock

        facade = VozCiudadanaFacade(db_mock)
        status = facade.get_proposal_status(2)

        assert proposal_mock.status == ProposalStatus.EXPIRED
        assert status["status"] == "expired"
        assert status["days_remaining"] == 0

    def test_firma_duplicada_rechazada(self):
        """No se permite que el mismo ciudadano firme dos veces."""
        op = build_signature_validator(BaseProposalOperation())
        data = {
            "deadline": datetime.utcnow() + timedelta(days=30),
            "signature_count": 100,
            "existing_signers": [7],
            "citizen_id": 7,
            "status": "collecting",
        }
        result = op.execute(data)
        assert result["success"] is False
        assert "ya firmaste" in result["error"].lower() or "firma" in result["error"].lower()
