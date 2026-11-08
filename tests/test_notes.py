"""Tests for the notes endpoints."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.notes.controller import NotesController, get_controller


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Give each test a client backed by a fresh, empty controller."""
    controller = NotesController()
    app.dependency_overrides[get_controller] = lambda: controller
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health_check(client: TestClient) -> None:
    """The root endpoint reports that the API is up."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_note(client: TestClient) -> None:
    """A created note can be fetched by its id."""
    response = client.post("/notes", json={"title": "Hello", "content": "World"})
    assert response.status_code == 201
    note = response.json()
    assert note["id"] == 1
    assert note["title"] == "Hello"

    response = client.get(f"/notes/{note['id']}")
    assert response.status_code == 200
    assert response.json() == note


def test_list_notes(client: TestClient) -> None:
    """Listing returns every note that was created."""
    client.post("/notes", json={"title": "First"})
    client.post("/notes", json={"title": "Second"})

    titles = [note["title"] for note in client.get("/notes").json()]
    assert titles == ["First", "Second"]


def test_update_note_changes_only_sent_fields(client: TestClient) -> None:
    """PATCH changes the given fields and leaves the rest alone."""
    note = client.post("/notes", json={"title": "Old", "content": "Keep me"}).json()

    response = client.patch(f"/notes/{note['id']}", json={"title": "New"})
    assert response.status_code == 200
    assert response.json()["title"] == "New"
    assert response.json()["content"] == "Keep me"


def test_delete_note(client: TestClient) -> None:
    """A deleted note can no longer be fetched."""
    note = client.post("/notes", json={"title": "Bye"}).json()

    assert client.delete(f"/notes/{note['id']}").status_code == 204
    assert client.get(f"/notes/{note['id']}").status_code == 404


def test_missing_note_returns_404(client: TestClient) -> None:
    """Asking for a note that doesn't exist gives 404."""
    assert client.get("/notes/999").status_code == 404
    assert client.patch("/notes/999", json={"title": "x"}).status_code == 404
    assert client.delete("/notes/999").status_code == 404


def test_empty_title_is_rejected(client: TestClient) -> None:
    """A note must have a title."""
    response = client.post("/notes", json={"title": ""})
    assert response.status_code == 422
