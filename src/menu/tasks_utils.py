from uuid import UUID

from redis import Redis
from sqlalchemy import delete, insert, select, update

from ..database import async_session
from .models import Dish, Menu, Submenu
from .redis_utils import delete_if_keys_exists


async def synchronize(values: list[list], redis: Redis) -> None:
    s_menus = {}
    s_submenus = {}
    s_dishes = {}
    current_menu = None
    current_submenu = None

    # Collect menus, submenus and dishes from document
    for row in values:
        start_index = 4  # Any number > 3 to avoid all checks
        if any(row):
            for i in range(len(row)):
                if row[i]:
                    start_index = i
                    break

        if start_index < 1:  # then it's menu
            [s_id, s_title, s_desc] = row[:3]
            s_menus[s_id] = {'title': s_title, 'description': s_desc}
            current_menu = s_id
        elif start_index < 2:  # then it's submenu
            [_, s_id, s_title, s_desc] = row[:4]
            s_submenus[s_id] = {'title': s_title, 'description': s_desc, 'menu_id': current_menu}
            current_submenu = s_id
        elif start_index < 3:  # then it's dish
            [_, _, s_id, s_title, s_desc, s_price] = row[:6]
            s_dishes[s_id] = {
                'title': s_title,
                'description': s_desc,
                'submenu_id': current_submenu,
                'price': str(s_price)
            }

    # Get menus from db
    async with async_session() as session:
        result = await session.execute(select(Menu))
        menus = result.scalars().all()

    # Sync menus existing in db
    for menu in menus:
        uuid = str(menu.id)
        if uuid not in s_menus:
            async with async_session() as session:
                await session.execute(delete(Menu).where(Menu.id == UUID(uuid)))
                await session.commit()

            delete_if_keys_exists(redis, 'list:*')
            delete_if_keys_exists(redis, f'{uuid}:*:*')
            continue

        elif not {
            'title': menu.title,
            'description': menu.description
        } == s_menus[uuid]:
            new_title, new_desc = s_menus[uuid]['title'], s_menus[uuid]['description']
            async with async_session() as session:
                await session.execute(update(Menu)
                                      .where(Menu.id == UUID(uuid))
                                      .values(title=new_title, description=new_desc))
                await session.commit()

            delete_if_keys_exists(redis, 'list:menu')
            delete_if_keys_exists(redis, f'{uuid}::')

        del s_menus[uuid]

    # Add new menus from document to db
    for pk, data in s_menus.items():
        async with async_session() as session:
            await session.execute(insert(Menu).values(id=UUID(pk),
                                                      title=data['title'],
                                                      description=data['description']))
            await session.commit()

        redis.delete('list:menu')

    # Get submenus from db
    async with async_session() as session:
        result = await session.execute(select(Submenu))
        submenus = result.scalars().all()

    # Sync submenus
    for submenu in submenus:
        uuid = str(submenu.id)
        if uuid not in s_submenus:
            async with async_session() as session:
                await session.execute(delete(Submenu).where(Submenu.id == UUID(uuid)))
                await session.commit()

            redis.delete(f'{submenu.menu_id}::')
            delete_if_keys_exists(redis, 'list:*')
            delete_if_keys_exists(redis, f'{submenu.menu_id}:{uuid}:*')
            continue
        elif not {
            'title': submenu.title,
            'description': submenu.description,
            'menu_id': submenu.menu_id
        } == s_submenus[uuid]:
            new_title, new_desc, new_menu_id = (s_submenus[uuid]['title'],
                                                s_submenus[uuid]['description'],
                                                s_submenus[uuid]['menu_id'])
            async with async_session() as session:
                await session.execute(update(Submenu)
                                      .where(Submenu.id == UUID(uuid))
                                      .values(title=new_title,
                                              description=new_desc,
                                              menu_id=new_menu_id))
                await session.commit()

            redis.delete(f'{submenu.menu_id}:{uuid}:')
            redis.delete('list:submenu')

        del s_submenus[uuid]

    # Add new submenus from document to db
    for pk, data in s_submenus.items():
        async with async_session() as session:
            await session.execute(insert(Submenu).values(id=UUID(pk),
                                                         title=data['title'],
                                                         description=data['description'],
                                                         menu_id=UUID(data['menu_id'])))
            await session.commit()

        redis.delete('list:menu')
        redis.delete('list:submenu')
        redis.delete(f'{data["menu_id"]}::')

    # Get dishes from db
    async with async_session() as session:
        result = await session.execute(select(Dish))
        dishes = result.scalars().all()

    # Sync dishes
    for dish in dishes:
        uuid = str(dish.id)
        if uuid not in s_dishes:
            async with async_session() as session:
                await session.execute(delete(Dish).where(Dish.id == UUID(uuid)))
                await session.commit()

            delete_if_keys_exists(redis, 'list:*')
            delete_if_keys_exists(redis, '*::')
            redis.delete(f'*:{dish.submenu_id}:*')
            continue
        elif not {
            'title': dish.title,
            'description': dish.description,
            'submenu_id': dish.submenu_id,
            'price': dish.price
        } == s_dishes[uuid]:
            new_title, new_desc, new_submenu_id, new_price = (s_dishes[uuid]['title'],
                                                              s_dishes[uuid]['description'],
                                                              s_dishes[uuid]['submenu_id'],
                                                              s_dishes[uuid]['price'])
            async with async_session() as session:
                await session.execute(update(Dish)
                                      .where(Dish.id == UUID(uuid))
                                      .values(title=new_title,
                                              description=new_desc,
                                              submenu_id=new_submenu_id,
                                              price=new_price))
                await session.commit()

            delete_if_keys_exists(redis, f'*:{dish.submenu_id}:{uuid}')
            redis.delete('list:dish')
        del s_dishes[uuid]

    # Add new dishes from document to db
    for pk, data in s_dishes.items():
        async with async_session() as session:
            await session.execute(insert(Dish).values(id=UUID(pk),
                                                      title=data['title'],
                                                      description=data['description'],
                                                      price=data['price'],
                                                      submenu_id=UUID(data['submenu_id'])))
            await session.commit()

        delete_if_keys_exists(redis, 'list:*')

        delete_if_keys_exists(redis, '*::')
        delete_if_keys_exists(redis, f'*:{data["submenu_id"]}:')
