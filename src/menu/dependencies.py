from src.menu.repository import DishRepository, MenuRepository, SubmenuRepository
from src.menu.service import DishService, MenuService, RestaurantService, SubmenuService


def get_menu_service() -> RestaurantService:
    return MenuService(MenuRepository())


def get_submenu_service() -> RestaurantService:
    return SubmenuService(SubmenuRepository())


def get_dish_service() -> RestaurantService:
    return DishService(DishRepository())
