from functools import reduce


def get_dishes_count_from_menu(menu):
    return 0 if not menu.submenus else reduce(lambda x, y: x + y,
                                              map(lambda x: len(x.dishes), menu.submenus))
