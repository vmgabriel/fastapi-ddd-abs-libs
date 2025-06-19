import datetime
from typing import List, Optional

import jwt

from src.domain.entrypoint import model as entrypoint_model
from src.domain.services import user

from . import model


class AuthPyJWT(model.AuthJWT):
    def encode(
        self,
        current_user: user.AuthUser,
        aud: List[str],
        expiration: Optional[datetime.timedelta] = None,
    ) -> model.EncodedJWT:
        current_datetime = datetime.datetime.now(tz=datetime.timezone.utc)
        if expiration:
            expiration_datetime = current_datetime + expiration
        else:
            expiration_datetime = (
                current_datetime + self.configuration.expiration_access_token
            )

        to_access_token = model.JWTData(
            user=current_user,
            aud=aud,
            gen=current_datetime,
            exp=expiration_datetime,
        )
        to_refresh_token = model.RefreshAuthUser(
            id=current_user.id,
            gen=current_datetime,
            exp=expiration_datetime,
        )

        if not self.configuration.auth_access_token_secret:
            raise ValueError("Require a auth_access_token_secret valid")
        if not self.configuration.auth_refresh_token_secret:
            raise ValueError("Require a auth_refresh_token_secret valid")

        access_token = jwt.encode(
            payload=to_access_token.dict(),
            key=self.configuration.auth_access_token_secret,
            algorithm="HS256",
        )
        refresh_token = jwt.encode(
            payload=to_refresh_token.dict(),
            key=self.configuration.auth_refresh_token_secret,
            algorithm="HS256",
        )

        return model.EncodedJWT(
            type=self.configuration.auth_type,
            access_token=access_token,
            refresh_token=refresh_token,
            generation=current_datetime,
            expiration=expiration_datetime,
        )

    def check_and_decode(
        self, token: str, allowed_aud: List[str]
    ) -> model.StatusCheckJWT:
        status = True
        message = "Active Token"
        data = None
        type = entrypoint_model.StatusType.OK

        try:
            decoded = jwt.decode(
                token,
                self.configuration.auth_access_token_secret,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
            data = model.JWTData(**decoded)
            if not data.has_permission(audiences=allowed_aud):
                raise jwt.exceptions.InvalidAudienceError()
        except jwt.exceptions.InvalidAudienceError:
            status = False
            message = "You don't have permissions for this resource"
            type = entrypoint_model.StatusType.NOT_PERMISSIONS
        except jwt.exceptions.ExpiredSignatureError:
            status = False
            message = "Not valid token, expired signature"
            type = entrypoint_model.StatusType.EXPIRED
        except jwt.exceptions.DecodeError as exc:
            status = False
            message = "Not Complete Information in Token"
            type = entrypoint_model.StatusType.NOT_COMPLETE
            print("Exception ", exc)
        except Exception as exc:
            # General Error
            self.logger.error(f"JWT Error - {exc}")
            status = False
            message = "Not Authorized"
            type = entrypoint_model.StatusType.NOT_AUTHORIZED

        return model.StatusCheckJWT(
            type=type,
            status=status,
            message=message,
            data=data,
        )

    def check_refresh_and_decode(self, token: str) -> model.StatusCheckJWT:
        status = True
        message = "Active Refresh Token"
        data = None
        type = entrypoint_model.StatusType.OK

        try:
            decoded = jwt.decode(
                jwt=token,
                key=self.configuration.auth_refresh_token_secret,
                algorithms=["HS256"],
            )
            data = model.RefreshAuthUser(**decoded)
        except jwt.exceptions.ExpiredSignatureError:
            status = False
            message = "Not valid token, expired signature"
            type = entrypoint_model.StatusType.EXPIRED
        except jwt.exceptions.DecodeError as exc:
            print(f"exc {exc}")
            status = False
            message = "Not Complete Information in Token"
            type = entrypoint_model.StatusType.NOT_COMPLETE
        except Exception as exc:
            # General Error
            self.logger.error(f"JWT Error - {exc}")
            status = False
            message = "Not Authorized"
            type = entrypoint_model.StatusType.NOT_AUTHORIZED

        return model.StatusCheckJWT(
            type=type,
            status=status,
            message=message,
            data=data,
        )
