from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel
from sqlmodel.main import Relationship

from aioauth_fastapi.storage.models import BaseTable
from aioauth_fastapi.users.crypto import make_random_password, pbkdf2, verify

if TYPE_CHECKING:
    from ..oauth2.models import AuthorizationCode, Client, Token


class UserAnonymous(BaseModel):
    @property
    def is_authenticated(self) -> bool:
        return False


class User(BaseTable, table=True):  # type: ignore
    is_superuser: bool = False
    is_blocked: bool = False
    is_active: bool = False

    username: str
    password: Optional[str] = None

    user_clients: List["Client"] = Relationship(back_populates="user")
    user_authorization_codes: List["AuthorizationCode"] = Relationship(
        back_populates="user"
    )
    user_tokens: List["Token"] = Relationship(back_populates="user")

    def set_password(self, password) -> None:
        """
        Sets users password using pbkdf2.
        """
        self.password = pbkdf2(password)

    def set_random_password(self) -> None:
        """
        Set random password.
        """
        password = make_random_password()
        self.password = pbkdf2(password)

    def verify_password(self, password: str) -> bool:
        """
        Verify users password
        """
        if self.password is None:
            return False
        return verify(password, self.password)

    @property
    def is_authenticated(self) -> bool:
        return True
