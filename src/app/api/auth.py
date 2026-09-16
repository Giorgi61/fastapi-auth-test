from fastapi import APIRouter
from starlette.requests import Request

from app.api.dependencies import AuthService, LoginForm
from app.oauths.oauth2 import oauth
from app.schemas.api.token import Token

router = APIRouter()


@router.post('/login', response_model=Token)
async def login_for_access_token(auth_serv: AuthService, user_form: LoginForm):

	username, password = user_form.username, user_form.password

	jwt_token = await auth_serv.login_for_access_token(username, password)

	return Token(access_token=jwt_token, token_type="bearer")


@router.get("/login/google")
async def login_via_google(request: Request):
	redirect_uri = request.url_for('auth_via_google')
	return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/authorize")
async def auth_via_google(request: Request, auth_service: AuthService):
	token = await oauth.google.authorize_access_token(request)
	user = token['userinfo']
	token = await auth_service.login_via_email_oauth(user)

	return Token(access_token=token, token_type='bearer')


