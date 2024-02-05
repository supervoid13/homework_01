import json
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException

from src.menu.dependencies import (
    get_dish_service,
    get_menu_service,
    get_submenu_service,
)
from src.menu.exceptions import NoSuchDishError, NoSuchMenuError, NoSuchSubmenuError
from src.menu.schemas import (
    DishCreateUpdate,
    DishRetrieve,
    MenuCreateUpdate,
    MenuRetrieve,
    SubmenuCreateUpdate,
    SubmenuRetrieve,
)
from src.menu.service import DishService, MenuService, SubmenuService

router = APIRouter(
    prefix='/api/v1/menus',
)


# Endpoints for Menu

@router.get('/', response_model=list[MenuRetrieve])
def get_menus(request: Request, service: MenuService = Depends(get_menu_service)):
    redis = request.app.state.redis
    menus = redis.lrange('list:menu', 0, -1)

    if menus:
        menus_utf8 = [menu.decode('utf-8') for menu in menus]
        menus_retrieve = [MenuRetrieve(**json.loads(menu)) for menu in menus_utf8]
        return menus_retrieve

    menus = service.retrieve_list()
    menus_retrieve = [menu.to_pydantic_model() for menu in menus]

    if menus_retrieve:
        redis.lpush('list:menu',
                    *[json.dumps(menu.model_dump()) for menu in menus_retrieve])

    return menus_retrieve


@router.get('/{menu_id}', response_model=MenuRetrieve)
def get_menu(menu_id: UUID, request: Request, service: MenuService = Depends(get_menu_service)):
    redis = request.app.state.redis
    menu = redis.hgetall(f'{menu_id}::')

    if menu:
        menu_utf8 = {k.decode('utf-8'): v.decode('utf-8') for k, v in menu.items()}
        return menu_utf8

    try:
        menu = service.retrieve_one(menu_id)
    except NoSuchMenuError:
        raise HTTPException(status_code=404, detail='menu not found')

    redis.hset(name=f'{menu_id}::', mapping=menu.to_pydantic_model().model_dump())

    return menu.to_pydantic_model()


@router.post('/', status_code=201, response_model=MenuRetrieve)
def add_menu(data: MenuCreateUpdate, request: Request, service: MenuService = Depends(get_menu_service)):
    menu = service.create_and_retrieve(data.model_dump())
    request.app.state.redis.delete('list:menu')

    return menu.to_pydantic_model()


@router.patch('/{menu_id}', response_model=MenuRetrieve)
def update_menu(menu_id: UUID,
                data: MenuCreateUpdate,
                request: Request,
                service: MenuService = Depends(get_menu_service)):
    try:
        menu = service.update_and_retrieve(menu_id, data.model_dump())
    except NoSuchMenuError:
        raise HTTPException(status_code=404, detail='menu not found')

    redis = request.app.state.redis
    redis.delete(f'{menu_id}::')
    redis.delete('list:menu')

    return menu.to_pydantic_model()


@router.delete('/{menu_id}')
def delete_menu(menu_id: UUID, request: Request, service: MenuService = Depends(get_menu_service)):

    service.delete(menu_id)

    redis = request.app.state.redis

    list_keys = redis.keys('list:*')
    if list_keys:
        redis.delete(*list_keys)

    keys = redis.keys(f'{menu_id}:*:*')
    if keys:
        redis.delete(*keys)

    return {'detail': 'menu has been deleted'}


# Endpoints for Submenu

@router.get('/{menu_id}/submenus', response_model=list[SubmenuRetrieve])
def get_submenus(menu_id: UUID,
                 request: Request,
                 service: SubmenuService = Depends(get_submenu_service)):

    redis = request.app.state.redis
    submenus = redis.lrange('list:submenu', 0, -1)

    if submenus:
        submenus_utf8 = [submenu.decode('utf-8') for submenu in submenus]
        submenus_retrieve = [SubmenuRetrieve(**json.loads(submenu)) for submenu in submenus_utf8]
        return submenus_retrieve

    submenus = service.retrieve_list()
    submenus_retrieve = [submenu.to_pydantic_model() for submenu in submenus]

    if submenus_retrieve:
        redis.lpush('list:submenu',
                    *[json.dumps(submenu.model_dump()) for submenu in submenus_retrieve])

    return submenus_retrieve


@router.get('/{menu_id}/submenus/{submenu_id}', response_model=SubmenuRetrieve)
def get_submenu(menu_id: UUID,
                submenu_id: UUID,
                request: Request,
                service: SubmenuService = Depends(get_submenu_service)):

    redis = request.app.state.redis
    submenu = redis.hgetall(f'{menu_id}:{submenu_id}:')

    if submenu:
        submenu_utf8 = {k.decode('utf-8'): v.decode('utf-8') for k, v in submenu.items()}
        return submenu_utf8

    try:
        submenu = service.retrieve_one(submenu_id)
    except NoSuchSubmenuError:
        raise HTTPException(status_code=404, detail='submenu not found')

    redis.hset(name=f'{menu_id}:{submenu_id}:', mapping=submenu.to_pydantic_model().model_dump())

    return submenu.to_pydantic_model()


@router.post('/{menu_id}/submenus', status_code=201, response_model=SubmenuRetrieve)
def add_submenu(menu_id: UUID,
                data: SubmenuCreateUpdate,
                request: Request,
                service: SubmenuService = Depends(get_submenu_service)):

    data = data.model_dump()
    data['menu_id'] = menu_id
    submenu = service.create_and_retrieve(data)

    redis = request.app.state.redis

    redis.delete('list:menu')
    redis.delete('list:submenu')
    redis.delete(f'{menu_id}::')

    return submenu.to_pydantic_model()


@router.patch('/{menu_id}/submenus/{submenu_id}', response_model=SubmenuRetrieve)
def update_submenu(menu_id: UUID,
                   submenu_id: UUID,
                   data: SubmenuCreateUpdate,
                   request: Request,
                   service: SubmenuService = Depends(get_submenu_service)):

    try:
        submenu = service.update_and_retrieve(submenu_id, data.model_dump())
    except NoSuchSubmenuError:
        raise HTTPException(status_code=404, detail='submenu not found')

    redis = request.app.state.redis
    redis.delete(f'{menu_id}:{submenu_id}:')
    redis.delete('list:submenu')

    return submenu.to_pydantic_model()


@router.delete('/{menu_id}/submenus/{submenu_id}')
def delete_submenu(menu_id: UUID,
                   submenu_id: UUID,
                   request: Request,
                   service: SubmenuService = Depends(get_submenu_service)) -> dict:

    service.delete(submenu_id)

    redis = request.app.state.redis

    list_keys = redis.keys('list:*')
    if list_keys:
        redis.delete(*list_keys)

    redis.delete(f'{menu_id}::')

    keys = redis.keys(f'{menu_id}:{submenu_id}:*')
    if keys:
        redis.delete(*keys)

    return {'detail': 'submenu has been deleted'}


# Endpoints for Dish

@router.get('/{menu_id}/submenus/{submenu_id}/dishes', response_model=list[DishRetrieve])
def get_dishes(menu_id: UUID,
               submenu_id: UUID,
               request: Request,
               service: DishService = Depends(get_dish_service)):

    redis = request.app.state.redis
    dishes = redis.lrange('list:dish', 0, -1)

    if dishes:
        dishes_utf8 = [dish.decode('utf-8') for dish in dishes]
        dishes_retrieve = [DishRetrieve(**json.loads(dish)) for dish in dishes_utf8]
        return dishes_retrieve

    dishes = service.retrieve_list()
    dishes_retrieve = [dish.to_pydantic_model() for dish in dishes]

    if dishes_retrieve:
        redis.lpush('list:dish',
                    *[json.dumps(dish.model_dump()) for dish in dishes_retrieve])

    return dishes_retrieve


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=DishRetrieve)
def get_dish(menu_id: UUID,
             submenu_id: UUID,
             dish_id: UUID,
             request: Request,
             service: DishService = Depends(get_dish_service)):

    redis = request.app.state.redis
    dish = redis.hgetall(f'{menu_id}:{submenu_id}:{dish_id}')

    if dish:
        dish_utf8 = {k.decode('utf-8'): v.decode('utf-8') for k, v in dish.items()}
        return dish_utf8

    try:
        dish = service.retrieve_one(dish_id)
    except NoSuchDishError:
        raise HTTPException(status_code=404, detail='dish not found')

    redis.hset(name=f'{menu_id}:{submenu_id}:{dish_id}', mapping=dish.to_pydantic_model().model_dump())

    return dish.to_pydantic_model()


@router.post('/{menu_id}/submenus/{submenu_id}/dishes', status_code=201, response_model=DishRetrieve)
def add_dish(menu_id: UUID,
             submenu_id: UUID,
             data: DishCreateUpdate,
             request: Request,
             service: DishService = Depends(get_dish_service)):

    data = data.model_dump()
    data['submenu_id'] = submenu_id

    dish = service.create_and_retrieve(data)

    redis = request.app.state.redis

    keys = redis.keys('list:*')
    if keys:
        redis.delete(*keys)

    redis.delete(f'{menu_id}::')
    redis.delete(f'{menu_id}:{submenu_id}:')

    return dish.to_pydantic_model()


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=DishRetrieve)
def update_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_id: UUID,
                data: DishCreateUpdate,
                request: Request,
                service: DishService = Depends(get_dish_service)):

    try:
        dish = service.update_and_retrieve(dish_id, data.model_dump())
    except NoSuchDishError:
        raise HTTPException(status_code=404, detail='dish not found')

    redis = request.app.state.redis
    redis.delete(f'{menu_id}:{submenu_id}:{dish_id}')
    redis.delete('list:dish')

    return dish.to_pydantic_model()


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_id: UUID,
                request: Request,
                service: DishService = Depends(get_dish_service)) -> dict:

    service.delete(dish_id)

    redis = request.app.state.redis

    list_keys = redis.keys('list:*')
    if list_keys:
        redis.delete(*list_keys)

    redis.delete(f'{menu_id}::')
    redis.delete(f'{menu_id}:{submenu_id}:')
    redis.delete(f'{menu_id}:{submenu_id}:{dish_id}')

    return {'detail': 'dish has been deleted'}
