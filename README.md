# Personal Notes API

A very simple FastAPI project for learning. You can create, read, update, and delete personal notes.

> Notes are stored **in memory**, so they disappear when the server stops. That keeps the project small.

## Project layout

The code is grouped **by feature** (`notes/`). Inside each feature it follows **MVC**:

```
app/
├── main.py              # Creates the app and plugs in each feature
└── notes/               # Everything about notes lives here
    ├── models.py        # M – what a note looks like (Pydantic models)
    ├── controller.py    # C – the logic: create/read/update/delete
    └── views.py         # V – the HTTP endpoints the client calls
tests/
└── test_notes.py
```

A request flows like this: **views** (HTTP) → **controller** (logic) → **models** (data).

## Setup (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

(macOS/Linux: `source .venv/bin/activate` instead of the second line.)

## Run the API

```powershell
uvicorn app.main:app --reload
```

Then open **http://127.0.0.1:8000/docs** to try every endpoint in your browser.

## Endpoints

| Method | Path              | What it does              |
|--------|-------------------|---------------------------|
| GET    | `/`               | Health check              |
| GET    | `/notes`          | List all notes            |
| POST   | `/notes`          | Create a note             |
| GET    | `/notes/{id}`     | Get one note              |
| PATCH  | `/notes/{id}`     | Update some fields        |
| DELETE | `/notes/{id}`     | Delete a note             |

Example note to send with POST:

```json
{ "title": "Groceries", "content": "Milk, eggs" }
```

## Code quality

```powershell
ruff check .        # find problems
ruff format .       # auto-format code
pytest              # run the tests
```
