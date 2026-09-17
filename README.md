# FastAPI Auth Test

A learning-oriented FastAPI sandbox focused on backend architecture, authentication, dependency injection, SQLAlchemy 2.0, and API design.

This project is intentionally experimental rather than production-ready. It was built as a testing ground for exploring different architectural approaches and understanding how the individual layers of a backend application interact.

## What I explored

* FastAPI dependency injection
* REST API design
* Async SQLAlchemy 2.0
* Repository and Service layers
* Generic repositories
* Specification-based filtering
* Relationship loading strategies (`selectinload`, `joinedload`)
* Pydantic v2 schemas and ORM integration
* Password hashing with Argon2
* JWT authentication
* OAuth 2.0 / Google authentication
* Authentication-related service abstractions and Protocols
* PostgreSQL/SQLite-compatible database access
* Project configuration with `pydantic-settings`
* Modern Python type annotations and generics

## Project structure

The application is organized into several layers:

```text
API
 ↓
Services
 ↓
Repositories
 ↓
SQLAlchemy models
 ↓
Database
```

Authentication and security-related functionality is separated into dedicated services and abstractions.

## Project status

The core functionality is implemented, but this repository should be considered a **learning sandbox**, not a production-ready application.

Some abstractions were intentionally introduced to explore different architectural ideas. As a result, the project may contain approaches that I would simplify or redesign in a production codebase.

The main goal of the project was not to build a complete product, but to understand the engineering decisions involved in designing a FastAPI backend.

## Tech stack

* Python 3.14+
* FastAPI
* Pydantic v2
* SQLAlchemy 2.0
* SQLite / aiosqlite
* PostgreSQL
* pwdlib / Argon2
* PyJWT
* Authlib
* uv
* Ruff
