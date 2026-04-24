from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.note import NoteCreateRequest, NoteResponse
from app.services.notes import create_note, list_notes

router = APIRouter(prefix="/internal/notes", tags=["internal-notes"])


@router.get("", response_model=list[NoteResponse])
def get_notes(
    user_id: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    return list_notes(db=db, user_id=user_id)


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def post_note(
    payload: NoteCreateRequest,
    db: Session = Depends(get_db),
):
    return create_note(db=db, payload=payload)
