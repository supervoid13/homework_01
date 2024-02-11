from functools import reduce

from .sheets_parser import get_rows


def get_dishes_count_from_menu(menu) -> int:
    return 0 if not menu.submenus else reduce(lambda x, y: x + y,
                                              map(lambda x: len(x.dishes), menu.submenus))


def get_discounts() -> dict[str, str]:
    values = get_rows()
    discounts = {}

    for row in values:
        if not (row[0] or row[1]):
            [_, _, s_id, *n, discount] = row[:7]
            if discount:
                discounts[s_id] = str(discount)

    return discounts
