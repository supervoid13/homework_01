from conftest import override_get_db

from src.menu.repository import DishRepository, MenuRepository, SubmenuRepository
from src.menu.service import DishService, MenuService, RestaurantService, SubmenuService


def override_get_menu_service() -> RestaurantService:
    repo = MenuRepository()
    repo.db = override_get_db  # type: ignore
    return MenuService(repo)


def override_get_submenu_service() -> RestaurantService:
    repo = SubmenuRepository()
    repo.db = override_get_db  # type: ignore
    return SubmenuService(repo)


def override_get_dish_service() -> RestaurantService:
    repo = DishRepository()
    repo.db = override_get_db  # type: ignore
    return DishService(repo)
