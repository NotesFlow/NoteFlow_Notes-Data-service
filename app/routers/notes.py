from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.note import Note
from app.schemas.notes import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter(prefix='/internal/notes', tags=['internal-notes'])


@router.post('', response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    note = Note(
        user_id=payload.user_id,
        title=payload.title,
        content=payload.content,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


@router.get('', response_model=list[NoteResponse])
def list_notes(
    user_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    return (
        db.query(Note)
        .filter(Note.user_id == user_id)
        .order_by(Note.created_at.desc())
        .all()
    )


@router.get('/{note_id}', response_model=NoteResponse)
def get_note(
    note_id: int,
    user_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id)
        .first()
    )

    if not note:
        raise HTTPException(status_code=404, detail='Note not found')

    return note


@router.put('/{note_id}', response_model=NoteResponse)
def update_note(
    note_id: int,
    payload: NoteUpdate,
    db: Session = Depends(get_db),
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == payload.user_id)
        .first()
    )

    if not note:
        raise HTTPException(status_code=404, detail='Note not found')

    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content

    db.commit()
    db.refresh(note)

    return note


@router.delete('/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    user_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id)
        .first()
    )

    if not note:
        raise HTTPException(status_code=404, detail='Note not found')

    db.delete(note)
    db.commit()

    return None
