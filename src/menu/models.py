import uuid
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from src.database import engine


class Base(DeclarativeBase):
    pass


uuid_pk = Annotated[uuid.UUID, mapped_column(primary_key=True, default=uuid.uuid4)]


class Menu(Base):
    __tablename__ = "menu"

    id: Mapped[uuid_pk]
    title: Mapped[str]
    description: Mapped[str]
    submenus: Mapped[list["Submenu"]] = relationship("Submenu", back_populates="menu",
                                                     cascade="all, delete")

    def __repr__(self):
        return f"{self.id}, {self.title}, {self.description}"


class Submenu(Base):
    __tablename__ = "submenu"

    id: Mapped[uuid_pk]
    title: Mapped[str]
    description: Mapped[str]
    menu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("menu.id"))
    menu: Mapped[Menu] = relationship("Menu", back_populates="submenus")
    dishes: Mapped[list["Dish"]] = relationship("Dish", back_populates="submenu",
                                                cascade="all,delete")


class Dish(Base):
    __tablename__ = "dish"

    id: Mapped[uuid_pk]
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[str]
    submenu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("submenu.id"))
    submenu: Mapped[Submenu] = relationship("Submenu", back_populates="dishes")


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


init_db()
