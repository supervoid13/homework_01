from conftest import async_session_test

from src.menu.repository import DishRepository, MenuRepository, SubmenuRepository
from src.menu.service import DishService, MenuService, SubmenuService


def override_get_menu_service() -> MenuService:
    repo = MenuRepository()
    repo.session_maker = async_session_test  # type: ignore
    return MenuService(repo)


def override_get_submenu_service() -> SubmenuService:
    repo = SubmenuRepository()
    repo.session_maker = async_session_test  # type: ignore
    return SubmenuService(repo)


def override_get_dish_service() -> DishService:
    repo = DishRepository()
    repo.session_maker = async_session_test  # type: ignore
    return DishService(repo)
