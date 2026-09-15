from app.service.protocols import UserServiceProtocol,  PasswordHasherProtocol, TokenServiceProtocol

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




	async def login_for_access_token(self, username: str, password: str) -> str:

		exp = InvalidCredentialsError('Invalid email or password')

		obj =  await self.user_serv.find_by_mail(username)

		if not obj or not self._hasher.verify_password(password, obj.hashed_password) :
			raise exp

		payload = {'sub': str(obj.id)}

		return self._token.create_access_token(data=payload)










