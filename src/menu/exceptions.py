class RestaurantException(Exception):
    pass


class NoSuchMenuError(RestaurantException):
    pass


class NoSuchSubmenuError(RestaurantException):
    pass


class NoSuchDishError(RestaurantException):
    pass
