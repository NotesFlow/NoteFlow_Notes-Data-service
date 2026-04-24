# NoteFlow Notes Data Service

Internal microservice responsible for note persistence in the `NoteFlow` project.

This service is part of the application layer and exists only to manage note data in PostgreSQL. It is intentionally simple and does not implement authentication or public-facing business logic.

## Purpose

`notes-data-service` is the direct persistence layer for notes.

Its responsibilities are:

- connect directly to PostgreSQL
- manage the `notes` table
- expose internal CRUD endpoints for notes
- filter operations by `user_id`

Its constraints are:

- it must not authenticate users
- it must not validate JWT tokens
- it must not expose public client endpoints
- it must not contain higher-level business logic that belongs in `notes-service`

## Service Role In The Architecture

Within the NoteFlow architecture:

- `auth-service` handles registration, login, JWT generation, and current-user validation
- `notes-service` exposes the public notes API, validates the authenticated user, and applies business rules
- `notes-data-service` performs direct database operations for notes

The expected flow is:

1. the client calls `notes-service`
2. `notes-service` validates the user and request payload
3. `notes-service` calls `notes-data-service`
4. `notes-data-service` reads or writes notes in PostgreSQL

## MVP Scope

The service must support the note persistence needs for:

- create note
- list notes
- update note
- delete note
- archive note
- pin note

This service is internal, so all operations are expected to receive a `user_id` provided by `notes-service`.

## Data Model

The minimum `notes` table structure is:

- `id`: integer primary key
- `user_id`: integer not null
- `title`: string(100) not null
- `content`: text not null
- `is_archived`: boolean default false
- `is_pinned`: boolean default false
- `created_at`: datetime
- `updated_at`: datetime

## Business Rules Enforced At This Layer

This service should keep its rules minimal and data-oriented:

- every read must be filtered by `user_id`
- every write must target only a note that belongs to the provided `user_id`
- `title` is required
- `content` may be empty

Authentication and user identity validation are out of scope here.

## Internal API Contract

These endpoints are internal and intended to be called by `notes-service`.

### `GET /internal/notes`

Returns the notes for a given user.

Expected query parameters:

- `user_id`

### `POST /internal/notes`

Creates a new note.

Expected request body:

```json
{
  "user_id": 1,
  "title": "My note",
  "content": "Example content"
}
```

### `PUT /internal/notes/{id}`

Updates an existing note that belongs to the provided `user_id`.

Expected request body:

```json
{
  "user_id": 1,
  "title": "Updated title",
  "content": "Updated content"
}
```

### `DELETE /internal/notes/{id}`

Deletes an existing note that belongs to the provided `user_id`.

Expected query parameters:

- `user_id`

### `PATCH /internal/notes/{id}/archive`

Updates the archive flag for a note that belongs to the provided `user_id`.

Expected request body:

```json
{
  "user_id": 1,
  "is_archived": true
}
```

### `PATCH /internal/notes/{id}/pin`

Updates the pin flag for a note that belongs to the provided `user_id`.

Expected request body:

```json
{
  "user_id": 1,
  "is_pinned": true
}
```

## Planned Response Shape

The implementation should aim for a clean, predictable response format based on the note resource itself.

Expected note shape:

```json
{
  "id": 1,
  "user_id": 1,
  "title": "My note",
  "content": "Example content",
  "is_archived": false,
  "is_pinned": false,
  "created_at": "2026-04-24T10:00:00Z",
  "updated_at": "2026-04-24T10:00:00Z"
}
```

## Planned Project Structure

The service will be implemented with a structure similar to:

```text
app/
  api/
    routes/
  core/
  db/
  models/
  schemas/
  services/
  main.py
requirements.txt
.env.example
README.md
```

The structure keeps responsibilities separate:

- `api/routes` for FastAPI endpoints
- `core` for configuration
- `db` for engine, session, and base setup
- `models` for SQLAlchemy models
- `schemas` for request and response models
- `services` for note data operations

## Configuration Contract

The service is expected to use environment variables for runtime configuration.

The initial contract is:

- `NOTES_DATA_SERVICE_HOST`
- `NOTES_DATA_SERVICE_PORT`
- `DATABASE_HOST`
- `DATABASE_PORT`
- `DATABASE_NAME`
- `DATABASE_USER`
- `DATABASE_PASSWORD`

See `.env.example` for the baseline values expected during local development.

## Implementation Order

This repository should be developed in small steps:

1. define the service contract and configuration
2. bootstrap the FastAPI application and database wiring
3. add the note model and table setup
4. implement create and list operations
5. implement update, delete, archive, and pin
6. test manually against PostgreSQL
7. finalize documentation

Each step should produce a clean, reviewable commit.

## Current Status

Current phase:

- service contract defined
- FastAPI bootstrap completed
- note model and table setup completed
- create and list endpoints completed
- remaining CRUD not implemented yet

The next step is to implement update, delete, archive, and pin operations.
