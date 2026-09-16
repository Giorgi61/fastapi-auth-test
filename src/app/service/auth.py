from app.service.protocols import (
	PasswordHasherProtocol,
	TokenServiceProtocol,
	UserServiceProtocol,
)


class InvalidCredentialsError(Exception):
	pass

class JWTExpiredError(Exception):
	pass

class AuthService[CanHash: PasswordHasherProtocol, UserService: UserServiceProtocol, TokenService: TokenServiceProtocol]:


	def __init__(self, user_serv: UserService,  hasher: CanHash, token: TokenService):
		self.user_serv = user_serv
		self._hasher = hasher
		self._token = token




	async def authenticate_by_access_token(self, token: str) -> dict:

		payload = self._token.verify_token(token)

		if not (payload):
			raise JWTExpiredError('JWT token is expired')



		return payload


	def _get_login_token(self, obj):


		payload = {'sub': str(obj.id)}

		return self._token.create_access_token(data=payload)


	async def login_for_access_token(self, username: str, password: str) -> str:

		exp = InvalidCredentialsError('Invalid email or password')

		obj =  await self.user_serv.find_by_mail(username)

		if not obj or not self._hasher.verify_password(password, obj.hashed_password):
			raise exp

		return self._get_login_token(obj)


	async def login_via_email_oauth(self, data: dict):

		user_mail = data['email']

		user = await self.user_serv.find_by_mail(user_mail)

		if user is None:
			mail = data['email']
			name_parts = data.get('name', '').split()
			name = name_parts[0] if name_parts else ''
			lastname = name_parts[1] if len(name_parts) > 1 else ''
			password = self._hasher.generate_random_password()

			data = {'email': mail, 'name':name, 'lastname': lastname,'password': password}

			user = await self.user_serv.create_user(data)



		return self._get_login_token(user)







