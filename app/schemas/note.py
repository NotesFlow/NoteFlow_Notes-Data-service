from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteCreateRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=100)
    content: str = ""


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    content: str
    is_archived: bool
    is_pinned: bool
    created_at: datetime
    updated_at: datetime
