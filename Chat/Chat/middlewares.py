from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from core.models import ChatKey
from channels.middleware import BaseMiddleware
from knox.auth import TokenAuthentication


@database_sync_to_async
def get_user(token):
    if token is None:
        return AnonymousUser()
    else:
        knox_auth = TokenAuthentication()
        # knox_auth.model = ChatKey
        user, _ = knox_auth.authenticate_credentials(token)
        return user


# class TokenAuthMiddleware:
#     def __init__(self, app):
#         self.app = app

#     async def __call__(self, scope, receive, send):
#         # query_params = dict(
#         #     (x.split("=") for x in scope["query_string"].decode().split("&"))
#         # )
#         # print(query_params)
#         # token = query_params.get("token", "").encode("utf-8")
#         scope["user"] = AnonymousUser()
#         return await self.app(scope, receive, send)
    
class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):

        # print(scope['headers'],"here ")
        try:
            token_key = dict(scope['headers'])[b'sec-websocket-protocol'].decode("utf-8").replace("Token'","").encode("utf-8")
            # print(token_key)
        except ValueError:
            token_key = None
        scope['user'] = await get_user(token_key)
        return await super().__call__(scope, receive, send)


import binascii
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from knox.crypto import hash_token
from knox.settings import CONSTANTS, knox_settings
from knox.auth import compare_digest


class ModelPluggableTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, token):
        msg = _("Invalid token.")
        token = token.decode("utf-8")
        for auth_token in self.model.objects.filter(
            token_key=token[: CONSTANTS.TOKEN_KEY_LENGTH]
        ):
            if self._cleanup_token(auth_token):
                continue

            try:
                digest = hash_token(token)
            except (TypeError, binascii.Error):
                raise exceptions.AuthenticationFailed(msg)
            if compare_digest(digest, auth_token.digest):
                if knox_settings.AUTO_REFRESH and auth_token.expiry:
                    self.renew_token(auth_token)
                return self.validate_user(auth_token)
        raise exceptions.AuthenticationFailed(msg)
