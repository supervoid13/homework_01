from conftest import override_get_db

from src.menu.repository import DishRepository, MenuRepository, SubmenuRepository
from src.menu.service import DishService, MenuService, SubmenuService


def override_get_menu_service() -> MenuService:
    repo = MenuRepository()
    repo.db = override_get_db  # type: ignore
    return MenuService(repo)


def override_get_submenu_service() -> SubmenuService:
    repo = SubmenuRepository()
    repo.db = override_get_db  # type: ignore
    return SubmenuService(repo)


def override_get_dish_service() -> DishService:
    repo = DishRepository()
    repo.db = override_get_db  # type: ignore
    return DishService(repo)
