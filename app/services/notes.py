from sqlalchemy.orm import Session

from app.models.note import Note
from app.schemas.note import NoteCreateRequest


def list_notes(db: Session, user_id: int) -> list[Note]:
    return (
        db.query(Note)
        .filter(Note.user_id == user_id)
        .order_by(Note.is_pinned.desc(), Note.updated_at.desc(), Note.id.desc())
        .all()
    )


def create_note(db: Session, payload: NoteCreateRequest) -> Note:
    note = Note(
        user_id=payload.user_id,
        title=payload.title,
        content=payload.content,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note
