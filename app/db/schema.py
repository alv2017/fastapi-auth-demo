from enum import Enum

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Role(str, Enum):
    basic = "basic"
    staff = "staff"
    admin = "admin"

    # def __str__(self):
    #     if self.basic:
    #         return self.basic.name
    #     elif self.staff:
    #         return self.staff.name
    #     elif self.admin:
    #         return self.admin.name
    #     else:
    #         raise ValueError("Invalid user role")


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(default=Role.basic)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
