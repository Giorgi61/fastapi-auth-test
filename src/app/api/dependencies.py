import app.service.dependencies as service_deps

from app.schemas.services.user_post_common import UserPostServiceSchema
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from typing import Annotated

PService = Annotated[service_deps.PostService, Depends(service_deps.get_post_service)]
UService =  Annotated[service_deps.UserService, Depends(service_deps.get_user_service)]
AuthService = Annotated[service_deps.AuthService, Depends(service_deps.get_auth_service)]

TokenJWT = Annotated[str, OAuth2PasswordBearer(tokenUrl='login')]


async def get_current_user(auth_serv: AuthService, user_serv: UService, token: TokenJWT, rels=False) -> UserPostServiceSchema:

	u_id = await auth_serv.authenticate_by_access_token(token)

	return await user_serv.get_user(u_id, relationships=rels)


current_user = Depends(get_current_user)