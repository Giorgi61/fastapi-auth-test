from authlib.integrations.starlette_client import OAuth

from app.core.config import settings

oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID.get_secret_value(),
    client_secret=settings.GOOGLE_CLIENT_SECRET.get_secret_value(),
    server_metadata_url=settings.GOOGLE_SERVER_METADATA_URL,
    client_kwargs={
        'scope': settings.GOOGLE_SCOPE,
    }
)