from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Proposal, Comment, Resource, ProposalStatus
from app.schemas.schemas import (
    ProposalCreate, ProposalResponse,
    CommentCreate, CommentResponse,
    ResourceCreate, ResourceResponse,
    SignatureCreate, SignatureResponse, FreezeResponse,
)
from app.patterns.facade import VozCiudadanaFacade
from app.routers.users import get_current_user
from app.models.models import User
from datetime import datetime

router = APIRouter(prefix="/proposals", tags=["proposals"])


@router.post("/", response_model=ProposalResponse, status_code=201)
def create_proposal(
    data: ProposalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    facade = VozCiudadanaFacade(db)
    proposal = facade.create_proposal(data.title, data.summary, data.full_text, current_user.id)
    return proposal


@router.get("/", response_model=List[ProposalResponse])
def list_proposals(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Proposal).offset(skip).limit(limit).all()


@router.get("/{proposal_id}", response_model=ProposalResponse)
def get_proposal(proposal_id: int, db: Session = Depends(get_db)):
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")
    return proposal


@router.get("/{proposal_id}/status")
def get_status(proposal_id: int, db: Session = Depends(get_db)):
    facade = VozCiudadanaFacade(db)
    return facade.get_proposal_status(proposal_id)


@router.post("/{proposal_id}/sign")
def sign_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    facade = VozCiudadanaFacade(db)
    result = facade.sign_proposal(proposal_id, current_user.id, ip_address="")
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


@router.post("/comments/", response_model=CommentResponse, status_code=201)
def add_comment(
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    proposal = db.query(Proposal).filter(Proposal.id == data.proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")
    comment = Comment(proposal_id=data.proposal_id, author_id=current_user.id, content=data.content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/{proposal_id}/comments", response_model=List[CommentResponse])
def get_comments(proposal_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.proposal_id == proposal_id).all()


@router.post("/resources/", response_model=ResourceResponse, status_code=201)
def add_resource(
    data: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resource = Resource(
        proposal_id=data.proposal_id,
        title=data.title,
        url=data.url,
        resource_type=data.resource_type,
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource
