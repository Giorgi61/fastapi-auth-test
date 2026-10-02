FROM python:3.14.7-alpine3.24
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
# Create "fastapi_user" and "fastapi_group"
RUN addgroup -S fastapi_user && adduser -S -G fastapi_user  \
    -h /home/fastapi_user -s /sbin/nologin fastapi_user #

# Create "/project" workdir and set ownership to fastapi_user

RUN mkdir /project && chown fastapi_user:fastapi_user /project

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /project

USER fastapi_user

COPY --chown=fastapi_user:fastapi_user ./pyproject.toml ./uv.lock ./

RUN uv sync --frozen --no-install-project

COPY --chown=fastapi_user:fastapi_user . .

RUN uv sync --frozen

ENTRYPOINT [ "uv", "run", "main" ]
