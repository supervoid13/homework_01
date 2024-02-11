from uuid import UUID

from src.menu.exceptions import (
    NoSuchDishError,
    NoSuchMenuError,
    NoSuchSubmenuError,
    RestaurantException,
)
from src.menu.models import Dish, Menu, Submenu
from src.repositories import AbstractRepository

from .crud import get_all_data_query


class RestaurantService:

    exception: type[RestaurantException]

    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    async def retrieve_list(self) -> list[Menu | Submenu | Dish]:
        return await self.repository.retrieve_list()

    async def retrieve_one(self, pk: UUID) -> Menu | Submenu | Dish:
        obj = await self.repository.retrieve_one(pk)

        if not obj:
            raise self.exception

        return obj

    async def create_and_retrieve(self, data: dict) -> Menu | Submenu | Dish:
        pk = await self.repository.create(data)
        obj = await self.repository.retrieve_one(pk)

        return obj

    async def update_and_retrieve(self, pk: UUID, data: dict) -> Menu | Submenu | Dish:
        await self.repository.update(pk, data)
        obj = await self.repository.retrieve_one(pk)

        if not obj:
            raise self.exception

        return obj

    async def delete(self, pk: UUID) -> None:
        await self.repository.delete(pk)


class MenuService(RestaurantService):
    exception = NoSuchMenuError

    async def retrieve_list_with_dependencies(self) -> list[Menu]:
        async with self.repository.session_maker() as session:  # type: ignore
            query = get_all_data_query()
            result = await session.execute(query)
            menus = result.unique().scalars().all()

            return menus


class SubmenuService(RestaurantService):
    exception = NoSuchSubmenuError

    async def retrieve_list_by_menu_id(self, menu_id: UUID) -> list[Submenu]:
        submenus = await self.repository.retrieve_list()

        return [submenu for submenu in submenus if submenu.menu_id == menu_id]


class DishService(RestaurantService):
    exception = NoSuchDishError

    async def retrieve_list_by_submenu_id(self, submenu_id: UUID) -> list[Submenu]:
        dishes = await self.repository.retrieve_list()

        return [dish for dish in dishes if dish.submenu_id == submenu_id]
