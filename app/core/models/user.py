from sqlalchemy.orm import Mapped,mapped_column

from core.models import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]