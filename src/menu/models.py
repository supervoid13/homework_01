import uuid
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.database import engine
from src.menu.schemas import DishRetrieve, MenuRetrieve, SubmenuRetrieve
from src.menu.utils import get_dishes_count_from_menu


class Base(DeclarativeBase):
    pass


uuid_pk = Annotated[uuid.UUID, mapped_column(primary_key=True, default=uuid.uuid4)]


class Menu(Base):
    __tablename__ = 'menu'

    id: Mapped[uuid_pk]
    title: Mapped[str]
    description: Mapped[str]
    submenus: Mapped[list['Submenu']] = relationship('Submenu', back_populates='menu',
                                                     cascade='all,delete')

    def to_pydantic_model(self) -> MenuRetrieve:
        return MenuRetrieve(
            id=str(self.id),
            title=self.title,
            description=self.description,
            submenus_count=len(self.submenus),
            dishes_count=get_dishes_count_from_menu(self)
        )


class Submenu(Base):
    __tablename__ = 'submenu'

    id: Mapped[uuid_pk]
    title: Mapped[str]
    description: Mapped[str]
    menu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('menu.id', ondelete='CASCADE'))
    menu: Mapped[Menu] = relationship('Menu', back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship('Dish', back_populates='submenu',
                                                cascade='all,delete')

    def to_pydantic_model(self) -> SubmenuRetrieve:
        return SubmenuRetrieve(
            id=str(self.id),
            title=self.title,
            description=self.description,
            dishes_count=len(self.dishes)
        )


class Dish(Base):
    __tablename__ = 'dish'

    id: Mapped[uuid_pk]
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[str]
    submenu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('submenu.id', ondelete='CASCADE'))
    submenu: Mapped[Submenu] = relationship('Submenu', back_populates='dishes')

    def to_pydantic_model(self) -> DishRetrieve:
        return DishRetrieve(
            id=str(self.id),
            title=self.title,
            description=self.description,
            price=self.price
        )


def init_db() -> None:
    Base.metadata.drop_all(bind=engine, checkfirst=True)
    Base.metadata.create_all(bind=engine)


init_db()
