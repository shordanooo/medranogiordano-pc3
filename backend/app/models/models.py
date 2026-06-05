from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class ProposalStatus(str, enum.Enum):
    DRAFT = "draft"
    COLLECTING = "collecting"
    FROZEN = "frozen"
    SUBMITTED = "submitted"
    EXPIRED = "expired"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String(8), unique=True, index=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    collective_name = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    proposals = relationship("Proposal", back_populates="author")
    signatures = relationship("Signature", back_populates="citizen")
    comments = relationship("Comment", back_populates="author")


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=False)
    full_text = Column(Text, nullable=False)
    status = Column(Enum(ProposalStatus), default=ProposalStatus.COLLECTING)
    signature_count = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime, nullable=False)
    frozen_at = Column(DateTime, nullable=True)
    crypto_hash = Column(String(512), nullable=True)
    submitted_to_congress = Column(Boolean, default=False)
    congress_ticket = Column(String(100), nullable=True)

    author = relationship("User", back_populates="proposals")
    signatures = relationship("Signature", back_populates="proposal")
    comments = relationship("Comment", back_populates="proposal")
    resources = relationship("Resource", back_populates="proposal")


class Signature(Base):
    __tablename__ = "signatures"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=False)
    citizen_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    signed_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=True)
    is_valid = Column(Boolean, default=True)

    proposal = relationship("Proposal", back_populates="signatures")
    citizen = relationship("User", back_populates="signatures")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    proposal = relationship("Proposal", back_populates="comments")
    author = relationship("User", back_populates="comments")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=False)
    title = Column(String(300), nullable=False)
    url = Column(String(500), nullable=True)
    file_path = Column(String(500), nullable=True)
    resource_type = Column(String(50), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    proposal = relationship("Proposal", back_populates="resources")
