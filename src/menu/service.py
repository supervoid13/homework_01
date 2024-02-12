import json
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
from .redis_utils import delete_if_keys_exists
from .schemas import MenuRetrieve, SubmenuRetrieve
from .utils import get_discounts


class RestaurantService:
    exception: type[RestaurantException]

    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    async def retrieve_list(self, **kwargs) -> list[Menu | Submenu | Dish]:
        return await self.repository.retrieve_list()

    async def retrieve_one(self, pk: UUID, **kwargs) -> Menu | Submenu | Dish:
        obj = await self.repository.retrieve_one(pk)

        if not obj:
            raise self.exception

        return obj

    async def create_and_retrieve(self, data: dict, **kwargs) -> Menu | Submenu | Dish:
        pk = await self.repository.create(data)
        obj = await self.repository.retrieve_one(pk)

        return obj

    async def update_and_retrieve(self, pk: UUID, data: dict, **kwargs) -> Menu | Submenu | Dish:
        await self.repository.update(pk, data)
        obj = await self.repository.retrieve_one(pk)

        if not obj:
            raise self.exception

        return obj

    async def delete(self, pk: UUID, **kwargs) -> None:
        await self.repository.delete(pk)


class MenuService(RestaurantService):
    exception = NoSuchMenuError

    async def retrieve_list(self, **kwargs) -> list[MenuRetrieve]:
        redis = kwargs['redis']
        menus = redis.lrange('list:menu', 0, -1)

        if menus:
            menus_utf8 = [menu.decode('utf-8') for menu in menus]
            menus_retrieve = [MenuRetrieve(**json.loads(menu)) for menu in menus_utf8]
            return menus_retrieve

        menus = await super().retrieve_list()
        menus_retrieve = [menu.to_pydantic_model() for menu in menus]

        if menus_retrieve:
            kwargs['background_tasks'].add_task(redis.lpush,
                                                'list:menu',
                                                *[json.dumps(menu.model_dump()) for menu in menus_retrieve])
        return menus_retrieve

    async def retrieve_one(self, pk: UUID, **kwargs) -> MenuRetrieve:
        redis = kwargs['redis']
        menu = redis.hgetall(f'{pk}::')

        if menu:
            menu_utf8 = {k.decode('utf-8'): v.decode('utf-8') for k, v in menu.items()}
            return MenuRetrieve(**menu_utf8)

        menu = await super().retrieve_one(pk)

        kwargs['background_tasks'].add_task(redis.hset,
                                            name=f'{pk}::',
                                            mapping=menu.to_pydantic_model().model_dump())
        return menu.to_pydantic_model()

    async def create_and_retrieve(self, data: dict, **kwargs) -> MenuRetrieve:
        redis = kwargs['redis']
        menu = await super().create_and_retrieve(data)
        kwargs['background_tasks'].add_task(redis.delete, 'list:menu')

        return menu.to_pydantic_model()

    async def update_and_retrieve(self, pk: UUID, data: dict, **kwargs) -> MenuRetrieve:
        redis = kwargs['redis']
        menu = await super().update_and_retrieve(pk, data)
        kwargs['background_tasks'].add_task(redis.delete, f'{pk}::')
        kwargs['background_tasks'].add_task(redis.delete, 'list:menu')

        return menu.to_pydantic_model()

    async def delete(self, pk: UUID, **kwargs) -> None:
        redis = kwargs['redis']
        await super().delete(pk)
        kwargs['background_tasks'].add_task(delete_if_keys_exists, redis, 'list:*')
        kwargs['background_tasks'].add_task(delete_if_keys_exists, redis, f'{pk}:*:*')

    async def retrieve_list_with_dependencies(self) -> list[Menu]:
        async with self.repository.session_maker() as session:  # type: ignore
            query = get_all_data_query()
            result = await session.execute(query)
            menus = result.unique().scalars().all()

        discounts = get_discounts()

        for menu in menus:
            for submenu in menu.submenus:
                for dish in submenu.dishes:
                    dish_id = str(dish.id)
                    if str(dish_id) in discounts:
                        price = float(dish.price)
                        discount = int(discounts[dish_id])
                        discount_price = price * (100 - discount) / 100
                        dish.price = str(discount_price)

        return menus


class SubmenuService(RestaurantService):
    exception = NoSuchSubmenuError

    async def retrieve_list_by_menu_id(self, menu_id: UUID, **kwargs) -> list[SubmenuRetrieve]:
        redis = kwargs['redis']
        submenus = redis.lrange('list:submenu', 0, -1)

        if submenus:
            submenus_utf8 = [submenu.decode('utf-8') for submenu in submenus]
            submenus_retrieve = [SubmenuRetrieve(**json.loads(submenu)) for submenu in submenus_utf8]
            return submenus_retrieve

        submenus = await self.repository.retrieve_list()
        submenus_of_menu = [submenu for submenu in submenus if submenu.menu_id == menu_id]
        submenus_retrieve = [submenu.to_pydantic_model() for submenu in submenus_of_menu]

        if submenus_retrieve:
            kwargs['background_tasks'].add_task(redis.lpush,
                                                'list:submenu',
                                                *[json.dumps(submenu.model_dump()) for submenu in submenus_retrieve])

        return submenus_retrieve

    async def retrieve_one(self, pk: UUID, **kwargs) -> SubmenuRetrieve:
        redis = kwargs['redis']
        menu_id = kwargs['menu_id']
        submenu = redis.hgetall(f'{menu_id}:{pk}:')

        if submenu:
            submenu_utf8 = {k.decode('utf-8'): v.decode('utf-8') for k, v in submenu.items()}
            return SubmenuRetrieve(**submenu_utf8)

        submenu = await super().retrieve_one(pk)

        kwargs['background_tasks'].add_task(redis.hset,
                                            name=f'{menu_id}:{pk}:',
                                            mapping=submenu.to_pydantic_model().model_dump())

        return submenu.to_pydantic_model()

    async def create_and_retrieve(self, data: dict, **kwargs) -> SubmenuRetrieve:
        redis = kwargs['redis']
        submenu = await super().create_and_retrieve(data)
        menu_id = kwargs['menu_id']

        kwargs['background_tasks'].add_task(redis.delete, 'list:menu')
        kwargs['background_tasks'].add_task(redis.delete, 'list:submenu')
        kwargs['background_tasks'].add_task(redis.delete, f'{menu_id}::')

        return submenu.to_pydantic_model()

    async def update_and_retrieve(self, pk: UUID, data: dict, **kwargs) -> SubmenuRetrieve:
        redis = kwargs['redis']
        submenu = await super().update_and_retrieve(pk, data)
        menu_id = kwargs['menu_id']
        kwargs['background_tasks'].add_task(redis.delete, f'{menu_id}:{pk}:')
        kwargs['background_tasks'].add_task(redis.delete, 'list:submenu')

        return submenu.to_pydantic_model()

    async def delete(self, pk: UUID, **kwargs) -> None:
        redis = kwargs['redis']
        await super().delete(pk)
        menu_id = kwargs['menu_id']

        kwargs['background_tasks'].add_task(delete_if_keys_exists, redis, 'list:*')
        kwargs['background_tasks'].add_task(redis.delete, f'{menu_id}::')
        kwargs['background_tasks'].add_task(delete_if_keys_exists, redis, f'{menu_id}:{pk}:*')


class DishService(RestaurantService):
    exception = NoSuchDishError

    async def retrieve_list_by_submenu_id(self, submenu_id: UUID) -> list[Submenu]:
        dishes = await self.repository.retrieve_list()

        return [dish for dish in dishes if dish.submenu_id == submenu_id]
