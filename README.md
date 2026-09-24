# FastAPI Auth Test

A learning-oriented **FastAPI backend sandbox** focused on authentication, dependency injection, SQLAlchemy 2.0, service/repository architecture, and modern Python typing.

> **Status:** personal learning project / experimental sandbox.  
> This repository is intentionally not presented as a production-ready application.

## 🎯 Purpose

The project was built as a testing ground for exploring how the layers of a backend application can interact:

- HTTP/API layer
- FastAPI dependency injection
- service layer
- repository layer
- SQLAlchemy models
- Pydantic schemas
- authentication and OAuth
- configuration and database access

Some abstractions are intentionally more complex than necessary. The goal was to **learn and experiment with architectural ideas**, not to optimize the codebase for production use.

## ✨ What I explored

- FastAPI dependency injection
- REST API design
- Async SQLAlchemy 2.0
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
- Modern Python type annotations and generics

## 🏗️ Architecture

The application roughly follows this flow:

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
                 │ data access   │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │   SQLAlchemy  │
                 │     models    │
                 └───────┬───────┘
                         │
                         ▼
                      Database
```

Authentication is separated into its own service and security abstractions. FastAPI dependencies are used to compose services and resolve the current authenticated user.

## 🔐 Authentication

The project contains two authentication flows:

### Username/password login

```http
POST /auth/login
```

The login flow:

1. receives OAuth2 password-form credentials;
2. looks up the user by email;
3. verifies the password using Argon2;
4. creates a JWT access token.

### Google OAuth 2.0

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

The exact request and response schemas are defined with Pydantic models.

## 🧩 Repository & Specification Pattern

One of the main experiments in this project is a generic repository abstraction.

Repositories provide reusable operations for SQLAlchemy models, while specifications describe filtering and relationship-loading requirements.

For example, the project has specifications for conditions such as:

```text
id_eq
created_at_gt
created_at_lt
updated_at_gt
updated_at_lt
```

Relationship loading can be expressed through:

```text
selectinload
joinedload
```

This was primarily an experiment in **generic programming, separation of concerns, and reusable data-access abstractions**.

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
├── LICENSE
├── README.md
├── pyproject.toml
└── uv.lock
```

## 🛠️ Tech Stack

- **Python 3.14+**
- **FastAPI**
- **Pydantic v2**
- **SQLAlchemy 2.0**
- **SQLite / aiosqlite**
- **pwdlib / Argon2**
- **PyJWT**
- **Authlib**
- **pydantic-settings**
- **uv**
- **Ruff**

The database layer is built around SQLAlchemy's async engine. SQLite is the currently configured database backend; other async SQLAlchemy dialects require their corresponding database driver.

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

## ⚙️ Configuration

The application loads configuration from a `.env` file in the project root using `pydantic-settings`.

Create:

```text
.env
```

Example:

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# DB_PARAMS is used as the base of the SQLAlchemy database URL.
DB_PARAMS=sqlite+aiosqlite://
DB_NAME=test.db

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_SERVER_METADATA_URL=https://accounts.google.com/.well-known/openid-configuration
GOOGLE_SCOPE=openid email profile

OAUTH_SECRET_KEY=your-oauth-secret-key
```

**Do not commit real secrets to the repository.**

The application builds the final database URI from `DB_PARAMS`, the project root, and `DB_NAME`.

## ▶️ Running the application

Start the development server with the project's console script:

```bash
uv run main
```

The application starts on:

```text
http://127.0.0.1:8000
```

FastAPI's interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI schema can also be inspected through:

```text
http://127.0.0.1:8000/openapi.json
```

## 🧪 Database initialization

The application creates the SQLAlchemy metadata during the FastAPI lifespan startup.

In other words, the current project uses:

```text
application startup
      │
      ▼
create_all()
      │
      ▼
database tables
```

This is convenient for a learning project, but it is **not a replacement for database migrations** in a production application.

## ⚠️ Current Limitations

This repository is intentionally a sandbox, so several things would need to be reconsidered before using it as a production service:

- no database migration system;
- limited automated test coverage;
- minimal error-handling strategy;
- authentication abstractions could be simplified;
- some generic abstractions are more complex than necessary;
- type annotations still need refinement;
- OAuth provider logic could be isolated more cleanly;
- production deployment configuration is not included;
- database and transaction handling would need a dedicated review.

These limitations are part of the project's learning context rather than hidden issues.

## 📚 Learning Focus

The project was mainly used to practice:

- designing a layered backend;
- dependency injection;
- asynchronous programming;
- SQLAlchemy 2.0;
- generic classes and protocols;
- repository abstractions;
- specification-based querying;
- authentication and authorization;
- JWT;
- OAuth 2.0 / OpenID Connect;
- Pydantic models;
- configuration management;
- modern Python typing.

The code should be viewed as a record of experimentation and learning rather than as a final architecture.

## 📄 License

This project is licensed under the **GNU General Public License v3.0**.

See the [LICENSE](./LICENSE) file for the full license text.
