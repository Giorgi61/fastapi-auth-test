# FastAPI Auth Test

A learning-oriented **FastAPI backend sandbox** for exploring authentication, dependency injection, asynchronous SQLAlchemy, layered architecture, generic repositories, specifications, OAuth 2.0, PostgreSQL, Docker, and modern Python typing.

> **Status:** personal learning project / experimental sandbox.  
> This repository is intentionally not presented as a production-ready application.

## 🎯 Purpose

This project is a practical sandbox for understanding how the main layers of a backend application fit together:

- HTTP / REST API
- FastAPI dependency injection
- service layer
- repository layer
- SQLAlchemy ORM
- Pydantic schemas
- authentication and OAuth
- PostgreSQL database access
- configuration management
- asynchronous programming
- Docker containerization

Some abstractions are intentionally more complex than necessary. The goal is to **learn and experiment with backend architecture and infrastructure**, not to optimize the codebase for production use.

## ✨ What the project explores

- FastAPI and REST API design
- FastAPI dependency injection with `Annotated` and `Depends`
- Async SQLAlchemy 2.0
- PostgreSQL with the async `psycopg` driver
- Repository and Service layers
- Generic repositories
- Specification-based filtering
- Relationship loading with `selectinload` and `joinedload`
- Pydantic v2 schemas with ORM integration
- Password hashing with Argon2
- JWT authentication
- OAuth 2.0 / Google authentication
- Authentication service abstractions and `Protocol`
- Async database access
- Project configuration with `pydantic-settings`
- Environment-based configuration
- Docker image construction with a non-root application user
- Docker Compose orchestration for the FastAPI app and PostgreSQL services
- PostgreSQL health checks, service startup ordering, a dedicated bridge network, and a named database volume
- `uv` dependency management inside the container
- Modern Python generics and type annotations

## 🏗️ Architecture

The application follows a layered backend structure:

```text
                         HTTP request
                              │
                              ▼
                      ┌───────────────┐
                      │   FastAPI API │
                      │    / routers  │
                      └───────┬───────┘
                              │
                              ▼
                      ┌───────────────┐
                      │    Services   │
                      │ business logic│
                      └───────┬───────┘
                              │
                              ▼
                      ┌───────────────┐
                      │  Repositories │
                      │   data access │
                      └───────┬───────┘
                              │
                              ▼
                      ┌───────────────┐
                      │   SQLAlchemy  │
                      │     models    │
                      └───────┬───────┘
                              │
                              ▼
                       PostgreSQL
```

FastAPI dependencies are used to compose repositories and services and to resolve the current authenticated user.

## 🔐 Authentication

The project contains two authentication flows.

### Username / password login

```http
POST /auth/login
```

The login flow:

1. receives OAuth2 password-form credentials;
2. looks up the user by email;
3. verifies the password using Argon2;
4. creates a JWT access token.

### Google OAuth 2.0 / OpenID Connect

```text
GET /auth/login/google
        │
        ▼
   Google OAuth
        │
        ▼
GET /auth/google/authorize
        │
        ▼
create/find local user
        │
        ▼
     JWT token
```

The OAuth integration uses **Authlib** and Google's OpenID Connect metadata.

## 🌐 API

Current routes are grouped into three areas:

| Prefix | Purpose |
| --- | --- |
| `/auth` | Password and Google authentication |
| `/users` | User creation, retrieval, update, and current-user access |
| `/posts` | Post creation and retrieval |

Examples:

```text
POST  /auth/login
GET   /auth/login/google
GET   /auth/google/authorize

GET   /users
GET   /users/me
GET   /users/{id}
GET   /users/{id}/posts
POST  /users
PATCH /users/{id}

GET   /posts
POST  /posts
```

Request and response validation is handled with Pydantic models.

## 🧩 Repository & Specification Pattern

One of the main experiments in this project is a generic repository abstraction.

Repositories provide reusable operations for SQLAlchemy models, while specifications describe filtering and relationship-loading requirements.

The specification layer includes conditions such as:

```text
id_eq
created_at_gt
created_at_lt
updated_at_gt
updated_at_lt
```

Relationship loading can be expressed through SQLAlchemy loader options such as:

```text
selectinload
joinedload
```

This is primarily an experiment in **generic programming, separation of concerns, reusable data-access abstractions, and typed service/repository boundaries**.

## 🗄️ Database

The current database backend is **PostgreSQL**.

The application builds its SQLAlchemy database URL from environment variables:

```text
DB_DRIVER=postgresql+psycopg
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_PORT=5432
DB_NAME=...
```

The database layer uses SQLAlchemy's asynchronous engine and `AsyncSession`:

```text
FastAPI
   │
   ▼
Async SQLAlchemy
   │
   ▼
psycopg
   │
   ▼
PostgreSQL
```

Database tables are currently created with SQLAlchemy's `metadata.create_all()` during FastAPI lifespan startup. This is convenient for the learning project, but it is **not a replacement for a migration system** such as Alembic.

## 🐳 Docker

The repository includes a Dockerfile for running the application in a container.

The current image setup:

- uses `python:3.14.7-alpine3.24`;
- copies `uv` from the official Astral image;
- creates a dedicated non-root `fastapi_user`;
- uses `/project` as the working directory;
- installs locked dependencies with `uv sync --frozen`;
- copies application files with the correct ownership;
- starts the application through the project's `main` console script.

The dependency installation is split into layers so that the dependency layer can be reused when application source files change without changing the lockfile or project metadata.

The `.dockerignore` excludes local virtual environments, Python cache files, Git metadata, and the local `.env` file from the build context.

### Docker Compose

The root-level `compose.yml` defines two services:

- **`app`** — builds the FastAPI image from the repository's `Dockerfile`, reads application settings from `.env`, and publishes port `8000` on the host.
- **`postgres`** — runs `postgres:16-alpine`, reads the database name/user/password from environment variables, and persists database files in the named `postgres-data` volume.

The application waits for PostgreSQL's health check to pass before starting. Both services share the `app-network` bridge network; the database is reachable from the application using `db` (or `database`) as its hostname. When running through Compose, set `DB_HOST=db` in `.env` rather than `localhost`.

#### Run with Docker Compose

1. Create a `.env` file in the repository root. Include the application settings shown in the [Configuration](#️-configuration) section, and set the database connection values for the Compose network:

   ```env
   DB_DRIVER=postgresql+psycopg
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=your-db-name
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   ```

   Use the same `DB_NAME`, `DB_USER`, and `DB_PASSWORD` values for the PostgreSQL service and the application's database connection. Keep secrets local; do not commit `.env`.

2. Build the image and start both services:

   ```bash
   docker compose up --build
   ```

3. Open the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

To stop the services, press `Ctrl+C` and run:

```bash
docker compose down
```

The named `postgres-data` volume is preserved when you run `docker compose down`. To also delete the database volume and its stored data, use `docker compose down --volumes`.

## ⚙️ Configuration

The application loads configuration from a `.env` file through `pydantic-settings`.

Create:

```text
.env
```

Example:

```env
APP_HOST=127.0.0.1
APP_PORT=8000

SECRET_KEY=your-app-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DB_DRIVER=postgresql+psycopg
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your-db-name

GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_SERVER_METADATA_URL=https://accounts.google.com/.well-known/openid-configuration
GOOGLE_SCOPE="openid email profile"

OAUTH_SECRET_KEY=your-oauth-secret-key
```

**Do not commit real secrets to the repository.**

The application constructs the final SQLAlchemy database URL from the PostgreSQL connection parameters.

## 📦 Installation

This project uses **uv**.

Clone the repository:

```bash
git clone https://github.com/Giorgi61/fastapi-auth-test.git
cd fastapi-auth-test
```

Install dependencies:

```bash
uv sync
```

Make sure a PostgreSQL instance is available and configure the database variables in `.env`. Alternatively, use the [Docker Compose setup](#docker-compose) to start the application and PostgreSQL together.

## ▶️ Running the application

Start the development server with the project's console script:

```bash
uv run main
```

The host and port are controlled by:

```env
APP_HOST=127.0.0.1
APP_PORT=8000
```

FastAPI's interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI schema is available at:

```text
http://127.0.0.1:8000/openapi.json
```

## 📁 Project Structure

```text
fastapi-auth-test/
│
├── src/
│   └── app/
│       ├── api/
│       │   ├── auth.py
│       │   ├── dependencies.py
│       │   ├── posts.py
│       │   └── users.py
│       │
│       ├── core/
│       │   ├── config.py
│       │   ├── database.py
│       │   ├── security.py
│       │   └── utils.py
│       │
│       ├── models/
│       │   ├── base.py
│       │   ├── posts.py
│       │   └── users.py
│       │
│       ├── oauths/
│       │   └── oauth2.py
│       │
│       ├── repository/
│       │   ├── base.py
│       │   ├── dependencies.py
│       │   ├── mixins.py
│       │   ├── posts.py
│       │   └── users.py
│       │
│       ├── schemas/
│       │   ├── api/
│       │   ├── common_constraints.py
│       │   └── services/
│       │
│       ├── service/
│       │   ├── auth.py
│       │   ├── base.py
│       │   ├── dependencies.py
│       │   ├── posts.py
│       │   ├── protocols.py
│       │   └── users.py
│       │
│       ├── specification/
│       │   ├── base.py
│       │   ├── posts.py
│       │   └── users.py
│       │
│       └── main.py
│
├── .dockerignore
├── .env.example
├── Dockerfile
├── compose.yml
├── LICENSE
├── README.md
├── pyproject.toml
└── uv.lock
```

## 🛠️ Tech Stack

### Application

- **Python 3.14+**
- **FastAPI**
- **Pydantic v2**
- **SQLAlchemy 2.0**
- **PostgreSQL**
- **psycopg 3**
- **pwdlib / Argon2**
- **PyJWT**
- **Authlib**
- **pydantic-settings**

### Tooling & Infrastructure

- **uv**
- **Ruff**
- **Docker**
- **Docker Compose** for the containerized application/database setup

## ⚠️ Current Limitations

This repository is intentionally a learning sandbox, so several areas would need further work before using it as a production service:

- no database migration system;
- limited automated test coverage;
- minimal error-handling strategy;
- authentication abstractions could be simplified;
- some generic abstractions are more complex than necessary;
- type annotations still need refinement;
- OAuth provider logic could be isolated more cleanly;
- production deployment configuration is not included;
- database and transaction handling would need a dedicated review;
- container orchestration and production runtime settings still need hardening.

These limitations are part of the project's learning context rather than hidden issues.

## 📚 Learning Focus

The project is mainly used to practice:

- designing a layered backend;
- dependency injection;
- asynchronous programming;
- SQLAlchemy 2.0;
- PostgreSQL and async database drivers;
- generic classes and protocols;
- repository abstractions;
- specification-based querying;
- authentication and authorization;
- JWT;
- OAuth 2.0 / OpenID Connect;
- Pydantic models;
- environment-based configuration;
- Docker and containerization;
- modern Python typing.

The code should be viewed as a record of experimentation and learning rather than as a final architecture.

## 📄 License

This project is licensed under the **GNU General Public License v3.0**.

See the [LICENSE](./LICENSE) file for the full license text.
