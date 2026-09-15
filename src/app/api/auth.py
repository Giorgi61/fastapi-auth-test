from fastapi import APIRouter
from app.api.dependencies import LoginForm, AuthService
from app.schemas.api.token import Token
router = APIRouter()


@router.post('/login', response_model=Token)
async def login_for_access_token(auth_serv: AuthService, user_form: LoginForm):

	username, password = user_form.username, user_form.password

	jwt_token = await auth_serv.login_for_access_token(username, password)

	return Token(access_token=jwt_token, token_type="bearer")
