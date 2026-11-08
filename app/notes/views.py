"""Views (the "V" in MVC): the HTTP endpoints for notes.

In an API, the "view" is the JSON the client sees. Each function here
receives an HTTP request, asks the controller to do the work, and
returns the result. Business logic stays in the controller.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.notes.controller import NoteNotFoundError, NotesController, get_controller
from app.notes.models import Note, NoteCreate, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

# A shortcut: "a NotesController, provided by get_controller()".
Controller = Annotated[NotesController, Depends(get_controller)]


def _not_found(error: NoteNotFoundError) -> HTTPException:
    """Turn a controller error into an HTTP 404 response."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.get("")
def list_notes(controller: Controller) -> list[Note]:
    """List all notes."""
    return controller.list_notes()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_note(data: NoteCreate, controller: Controller) -> Note:
    """Create a new note."""
    return controller.create_note(data)


@router.get("/{note_id}")
def get_note(note_id: int, controller: Controller) -> Note:
    """Get one note by its id."""
    try:
        return controller.get_note(note_id)
    except NoteNotFoundError as error:
        raise _not_found(error) from error


@router.patch("/{note_id}")
def update_note(note_id: int, data: NoteUpdate, controller: Controller) -> Note:
    """Update some or all fields of a note."""
    try:
        return controller.update_note(note_id, data)
    except NoteNotFoundError as error:
        raise _not_found(error) from error


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, controller: Controller) -> None:
    """Delete a note."""
    try:
        controller.delete_note(note_id)
    except NoteNotFoundError as error:
        raise _not_found(error) from error
