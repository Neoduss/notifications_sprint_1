from http import HTTPStatus
from typing import Dict

import jwt
from fastapi import HTTPException

from app.core.config import Settings

settings = Settings()


class Auth:
    secret = settings.jwt_secret_key

    def decode_token(self, token: str) -> Dict[str, int]:
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if payload['type'] == 'access':
                return payload['app_id']
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token')
