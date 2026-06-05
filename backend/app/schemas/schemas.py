from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional, List
from app.models.models import ProposalStatus


class UserCreate(BaseModel):
    dni: str
    full_name: str
    email: EmailStr
    password: str
    collective_name: Optional[str] = None

    @field_validator("dni")
    @classmethod
    def validate_dni(cls, v):
        if not v.isdigit() or len(v) != 8:
            raise ValueError("DNI debe tener exactamente 8 dígitos numéricos")
        return v


class UserResponse(BaseModel):
    id: int
    dni: str
    full_name: str
    email: str
    collective_name: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class ProposalCreate(BaseModel):
    title: str
    summary: str
    full_text: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("El título debe tener al menos 10 caracteres")
        return v.strip()


class ProposalResponse(BaseModel):
    id: int
    title: str
    summary: str
    full_text: str
    status: ProposalStatus
    signature_count: int
    author_id: int
    created_at: datetime
    deadline: datetime
    frozen_at: Optional[datetime]
    crypto_hash: Optional[str]
    submitted_to_congress: bool
    congress_ticket: Optional[str]

    model_config = {"from_attributes": True}


class SignatureCreate(BaseModel):
    proposal_id: int


class SignatureResponse(BaseModel):
    id: int
    proposal_id: int
    citizen_id: int
    signed_at: datetime
    is_valid: bool

    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    proposal_id: int
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        if len(v.strip()) < 5:
            raise ValueError("El comentario debe tener al menos 5 caracteres")
        return v.strip()


class CommentResponse(BaseModel):
    id: int
    proposal_id: int
    author_id: int
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ResourceCreate(BaseModel):
    proposal_id: int
    title: str
    url: Optional[str] = None
    resource_type: str


class ResourceResponse(BaseModel):
    id: int
    proposal_id: int
    title: str
    url: Optional[str]
    resource_type: str
    uploaded_at: datetime

    model_config = {"from_attributes": True}


class FreezeResponse(BaseModel):
    proposal_id: int
    crypto_hash: str
    frozen_at: datetime
    congress_ticket: str
    message: str
