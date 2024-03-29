"""
Class business logic for json web tokens
"""

from app.auth.schemas.jwt import TokensSchema
from core.helpers.token import token_checker
from core.helpers.token import TokenHelper
from core.exceptions.base import UnauthorizedException
from core.helpers.hashids import encode, decode_single


class JwtService:
    """
    Class for JSON Web Token business logic
    """

    def create_login_tokens(self, user_id: int):
        """
        Create a new set of access and refresh tokens for the given user

        Args:
            user_id (int): The ID of the user to create tokens for

        Returns:
            TokensSchema: A new set of tokens containing the access and refresh tokens
        """

        return TokensSchema(
            access_token=TokenHelper.encode_access(payload={"user_id": user_id}),
            refresh_token=TokenHelper.encode_refresh(payload={"user_id": user_id}),
        )
    
    def refresh_tokens(
        self,
        refresh_token: str,
    ) -> TokensSchema:
        """
        Create a new refresh token

        Args:
            refresh_token (str): The old refresh token to use as a template for the new
            refresh token.

        Returns:
            TokensSchema: A new set of tokens containing the new access token and 
            refresh token.

        Raises:
            DecodeTokenException: If the old refresh token cannot be decoded
            UnauthorizedException: If the new token ID cannot be generated
        """
        refresh_token = TokenHelper.decode(token=refresh_token)

        user_id = decode_single(refresh_token.get("user_id"))
        user_id = encode(user_id)
        
        try:
            jti = token_checker.generate_add(refresh_token.get("jti"))

        except (ValueError, KeyError) as exc:
            raise UnauthorizedException from exc

        return TokensSchema(
            access_token=TokenHelper.encode_access(payload={"user_id": user_id}),
            refresh_token=TokenHelper.encode_refresh(
                payload={"jti": jti, "user_id": user_id}
            ),
        )
