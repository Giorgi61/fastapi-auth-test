from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import app.service.dependencies as service_deps
from app.schemas.services.user_post_common import UserPostServiceSchema

PService = Annotated[service_deps.PostService, Depends(service_deps.get_post_service)]
UService =  Annotated[service_deps.UserService, Depends(service_deps.get_user_service)]
AuthService = Annotated[service_deps.AuthService, Depends(service_deps.get_auth_service)]

TokenJWT = Annotated[str, OAuth2PasswordBearer(tokenUrl='auth/login')]
LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_current_user_id(auth_serv: AuthService, token: TokenJWT) -> int:
	payload = await auth_serv.authenticate_by_access_token(token)

	return int(payload['sub'])

CurrentUId = Annotated[int, Depends(get_current_user_id)]

async def get_current_user( user_id: CurrentUId, user_serv: UService, rels=False) -> UserPostServiceSchema:


	return await user_serv.get_user(int(user_id), relationships=rels)

CurrentUser = Annotated[UserPostServiceSchema, Depends(get_current_user)]

