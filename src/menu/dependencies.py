from src.menu.repository import DishRepository, MenuRepository, SubmenuRepository
from src.menu.service import DishService, MenuService, SubmenuService


def get_menu_service() -> MenuService:
    return MenuService(MenuRepository())


def get_submenu_service() -> SubmenuService:
    return SubmenuService(SubmenuRepository())


def get_dish_service() -> DishService:
    return DishService(DishRepository())
