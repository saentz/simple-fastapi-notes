"""Controller (the "C" in MVC): the logic for managing notes.

The controller knows *how* to create, read, update, and delete notes.
It knows nothing about HTTP; that is the view's job.

Notes are kept in memory (a plain dictionary), so they disappear when
the server restarts. That keeps this project simple. Swapping in a real
database later only requires changing this file.
"""

from datetime import UTC, datetime

from app.notes.models import Note, NoteCreate, NoteUpdate


class NoteNotFoundError(Exception):
    """Raised when a note with the requested id does not exist."""

    def __init__(self, note_id: int) -> None:
        """Store the missing id and build a readable message."""
        self.note_id = note_id
        super().__init__(f"Note {note_id} not found")


class NotesController:
    """Create, read, update, and delete notes stored in memory."""

    def __init__(self) -> None:
        """Start with no notes. The first note will get id 1."""
        self._notes: dict[int, Note] = {}
        self._next_id = 1

    def list_notes(self) -> list[Note]:
        """Return all notes, oldest first."""
        return list(self._notes.values())

    def get_note(self, note_id: int) -> Note:
        """Return one note by id.

        Raises:
            NoteNotFoundError: If no note has this id.
        """
        note = self._notes.get(note_id)
        if note is None:
            raise NoteNotFoundError(note_id)
        return note

    def create_note(self, data: NoteCreate) -> Note:
        """Create a new note and return it."""
        now = datetime.now(UTC)
        note = Note(
            id=self._next_id,
            title=data.title,
            content=data.content,
            created_at=now,
            updated_at=now,
        )
        self._notes[note.id] = note
        self._next_id += 1
        return note

    def update_note(self, note_id: int, data: NoteUpdate) -> Note:
        """Change only the fields the client sent, then return the note.

        Raises:
            NoteNotFoundError: If no note has this id.
        """
        note = self.get_note(note_id)
        changes = data.model_dump(exclude_unset=True)
        updated = note.model_copy(
            update={**changes, "updated_at": datetime.now(UTC)},
        )
        self._notes[note_id] = updated
        return updated

    def delete_note(self, note_id: int) -> None:
        """Delete a note.

        Raises:
            NoteNotFoundError: If no note has this id.
        """
        self.get_note(note_id)  # Raises if the note doesn't exist.
        del self._notes[note_id]


# One shared controller for the whole app, so every request sees the same notes.
_controller = NotesController()


def get_controller() -> NotesController:
    """Give FastAPI the shared controller (used with ``Depends``).

    Using a function instead of importing ``_controller`` directly lets
    tests swap in a fresh controller.
    """
    return _controller
