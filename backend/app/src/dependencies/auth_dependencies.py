from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.src.database.repositories.user_repository import UserRepository
from app.src.security.auth_security import AuthSecurity


class AuthDependency:

     __oauth_bearer = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

     @staticmethod
     async def get_current_user(token: str = Depends(__oauth_bearer)):
          try:
               payload = AuthSecurity.decode_jwt_token(token)
               if not payload:
                    raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail={'status': 'fail', 'message': 'User not found'})
               # otherwise retrieve user info
               decrypted_payload = AuthSecurity.decrypt_data(payload)
               # get the user id of user
               user_id = decrypted_payload.get('user_id')
               data = await UserRepository.find_user_by_id(user_id)

               if not data:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail={'status': 'fail', 'message': 'User not found'})
               # return user_id
               return data
          except Exception as e:
               raise e
