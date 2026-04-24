# NoteFlow Notes Data Service

Internal microservice for note persistence in the NoteFlow project.

This service talks directly to PostgreSQL and exposes internal CRUD endpoints for notes.

## Responsibilities

This service is responsible for:

- direct interaction with PostgreSQL
- creating notes
- listing notes by `user_id`
- reading a note by `id` and `user_id`
- updating notes
- deleting notes

This service is not responsible for:

- user registration
- login
- JWT validation
- public API gateway routing
- authorization token parsing

`notes-service` should validate the user with `auth-service`, then call this service using the authenticated user's `user_id`.

## Endpoints

```text
GET    /health
GET    /health/db
POST   /internal/notes
GET    /internal/notes?user_id=1
GET    /internal/notes/{note_id}?user_id=1
PUT    /internal/notes/{note_id}
DELETE /internal/notes/{note_id}?user_id=1
```

## Note Model

```text
notes
- id
- user_id
- title
- content
- created_at
- updated_at
```

## Local Development

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

For running directly on your machine:

```env
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
```

For running this service inside Docker while PostgreSQL runs on your Mac host:

```env
DATABASE_HOST=host.docker.internal
DATABASE_PORT=5432
```

If PostgreSQL is exposed as `5433->5432`, use:

```env
DATABASE_PORT=5433
```

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003
```

Swagger UI:

```text
http://127.0.0.1:8003/docs
```

## Docker

Build:

```bash
docker build -t noteflow-notes-data-service .
```

Run:

```bash
docker run --rm -p 8003:8003 --env-file .env noteflow-notes-data-service
```

## Tests

```bash
pytest
```

## Example Requests

Create note:

```bash
curl -X POST http://127.0.0.1:8003/internal/notes \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"title":"First note","content":"Hello NoteFlow"}'
```

List notes:

```bash
curl "http://127.0.0.1:8003/internal/notes?user_id=1"
```

Get note:

```bash
curl "http://127.0.0.1:8003/internal/notes/1?user_id=1"
```

Update note:

```bash
curl -X PUT http://127.0.0.1:8003/internal/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"title":"Updated note","content":"Updated content"}'
```

Delete note:

```bash
curl -X DELETE "http://127.0.0.1:8003/internal/notes/1?user_id=1"
```
