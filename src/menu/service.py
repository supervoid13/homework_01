from uuid import UUID

from src.menu.exceptions import (
    NoSuchDishError,
    NoSuchMenuError,
    NoSuchSubmenuError,
    RestaurantException,
)
from src.menu.models import Dish, Menu, Submenu
from src.repositories import AbstractRepository


class RestaurantService:

    exception: type[RestaurantException]

    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def retrieve_list(self) -> list[Menu | Submenu | Dish]:
        return self.repository.retrieve_list()

    def retrieve_one(self, pk: UUID) -> Menu | Submenu | Dish:
        obj = self.repository.retrieve_one(pk)

        if not obj:
            raise self.exception

        return obj

    def create_and_retrieve(self, data: dict) -> Menu | Submenu | Dish:
        pk = self.repository.create(data)
        obj = self.repository.retrieve_one(pk)

        return obj

    def update_and_retrieve(self, pk: UUID, data: dict) -> Menu | Submenu | Dish:
        self.repository.update(pk, data)
        obj = self.repository.retrieve_one(pk)

        if not obj:
            raise self.exception

        return obj

    def delete(self, pk: UUID) -> None:
        self.repository.delete(pk)


class MenuService(RestaurantService):
    exception = NoSuchMenuError


class SubmenuService(RestaurantService):
    exception = NoSuchSubmenuError


class DishService(RestaurantService):
    exception = NoSuchDishError
