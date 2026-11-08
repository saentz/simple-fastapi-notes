"""Models (the "M" in MVC): the shape of a note.

Pydantic models describe what data looks like. FastAPI uses them to
validate incoming requests and to format outgoing responses.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    """Data the client sends to create a note."""

    title: str = Field(min_length=1, max_length=100, examples=["Groceries"])
    content: str = Field(default="", max_length=10_000, examples=["Milk, eggs"])


class NoteUpdate(BaseModel):
    """Data the client sends to update a note.

    Every field is optional, so the client only sends what it wants to change.
    """

    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, max_length=10_000)


class Note(BaseModel):
    """A note as stored and returned by the API."""

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
