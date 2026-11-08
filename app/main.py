"""Application entry point: creates the FastAPI app and plugs in features.

Run it with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.notes.views import router as notes_router

app = FastAPI(
    title="Personal Notes API",
    description="A very simple API for writing and managing personal notes.",
    version="0.1.0",
)

# Each feature brings its own router. To add a feature, include its router here.
app.include_router(notes_router)


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    """Confirm the API is running."""
    return {"status": "ok"}
