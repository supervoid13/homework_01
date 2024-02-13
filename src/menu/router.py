from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.exceptions import HTTPException

from .dependencies import get_dish_service, get_menu_service, get_submenu_service
from .exceptions import NoSuchDishError, NoSuchMenuError, NoSuchSubmenuError
from .responses import DISH_NOT_FOUND, MENU_NOT_FOUND, SUBMENU_NOT_FOUND
from .schemas import (
    DishCreateUpdate,
    DishRetrieve,
    MenuCreateUpdate,
    MenuRetrieve,
    SubmenuCreateUpdate,
    SubmenuRetrieve,
)
from .service import DishService, MenuService, SubmenuService

router = APIRouter(
    prefix='/api/v1/menus',
)


# Endpoints for Menu

@router.get('/', response_model=list[MenuRetrieve])
async def get_menus(request: Request,
                    background_tasks: BackgroundTasks,
                    service: MenuService = Depends(get_menu_service)) -> list[MenuRetrieve]:
    menus = await service.retrieve_list(background_tasks=background_tasks,
                                        redis=request.app.state.redis)
    return menus


@router.get('/dependencies')
async def get_menus_with_dependencies(service: MenuService = Depends(get_menu_service)) -> list:
    menus_with_dependencies = await service.retrieve_list_with_dependencies()
    return menus_with_dependencies


@router.get('/{menu_id}',
            response_model=MenuRetrieve,
            responses={**MENU_NOT_FOUND})
async def get_menu(menu_id: UUID,
                   request: Request,
                   background_tasks: BackgroundTasks,
                   service: MenuService = Depends(get_menu_service)) -> MenuRetrieve:
    try:
        menu = await service.retrieve_one(menu_id,
                                          background_tasks=background_tasks,
                                          redis=request.app.state.redis)
    except NoSuchMenuError:
        raise HTTPException(status_code=404, detail='menu not found')

    return menu


@router.post('/', status_code=201, response_model=MenuRetrieve)
async def add_menu(data: MenuCreateUpdate,
                   request: Request,
                   background_tasks: BackgroundTasks,
                   service: MenuService = Depends(get_menu_service)) -> MenuRetrieve:
    menu = await service.create_and_retrieve(data.model_dump(),
                                             background_tasks=background_tasks,
                                             redis=request.app.state.redis)
    return menu


@router.patch('/{menu_id}',
              response_model=MenuRetrieve,
              responses={**MENU_NOT_FOUND})
async def update_menu(menu_id: UUID,
                      data: MenuCreateUpdate,
                      request: Request,
                      background_tasks: BackgroundTasks,
                      service: MenuService = Depends(get_menu_service)) -> MenuRetrieve:
    try:
        menu = await service.update_and_retrieve(menu_id,
                                                 data.model_dump(),
                                                 background_tasks=background_tasks,
                                                 redis=request.app.state.redis)
    except NoSuchMenuError:
        raise HTTPException(status_code=404, detail='menu not found')

    return menu


@router.delete('/{menu_id}', responses={200: {'description': 'Menu successfully deleted',
                                              'content': {
                                                  'application/json': {
                                                      'example': {'detail': 'menu has been deleted'}
                                                  }
                                              }}
                                        })
async def delete_menu(menu_id: UUID,
                      request: Request,
                      background_tasks: BackgroundTasks,
                      service: MenuService = Depends(get_menu_service)) -> dict:
    await service.delete(menu_id,
                         background_tasks=background_tasks,
                         redis=request.app.state.redis)

    return {'detail': 'menu has been deleted'}


# Endpoints for Submenu

@router.get('/{menu_id}/submenus', response_model=list[SubmenuRetrieve])
async def get_submenus(menu_id: UUID,
                       request: Request,
                       background_tasks: BackgroundTasks,
                       service: SubmenuService = Depends(get_submenu_service)) -> list[SubmenuRetrieve]:
    submenus = await service.retrieve_list_by_menu_id(menu_id,
                                                      background_tasks=background_tasks,
                                                      redis=request.app.state.redis)
    return submenus


@router.get('/{menu_id}/submenus/{submenu_id}',
            response_model=SubmenuRetrieve,
            responses={**SUBMENU_NOT_FOUND})
async def get_submenu(menu_id: UUID,
                      submenu_id: UUID,
                      request: Request,
                      background_tasks: BackgroundTasks,
                      service: SubmenuService = Depends(get_submenu_service)) -> SubmenuRetrieve:
    try:
        submenu = await service.retrieve_one(submenu_id,
                                             background_tasks=background_tasks,
                                             menu_id=menu_id,
                                             redis=request.app.state.redis)
    except NoSuchSubmenuError:
        raise HTTPException(status_code=404, detail='submenu not found')

    return submenu


@router.post('/{menu_id}/submenus', status_code=201, response_model=SubmenuRetrieve)
async def add_submenu(menu_id: UUID,
                      data: SubmenuCreateUpdate,
                      request: Request,
                      background_tasks: BackgroundTasks,
                      service: SubmenuService = Depends(get_submenu_service)) -> SubmenuRetrieve:
    data = data.model_dump()
    data['menu_id'] = menu_id
    submenu = await service.create_and_retrieve(data,
                                                background_tasks=background_tasks,
                                                menu_id=menu_id,
                                                redis=request.app.state.redis)

    return submenu


@router.patch('/{menu_id}/submenus/{submenu_id}',
              response_model=SubmenuRetrieve,
              responses={**SUBMENU_NOT_FOUND})
async def update_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         data: SubmenuCreateUpdate,
                         request: Request,
                         background_tasks: BackgroundTasks,
                         service: SubmenuService = Depends(get_submenu_service)) -> SubmenuRetrieve:
    try:
        submenu = await service.update_and_retrieve(submenu_id,
                                                    data.model_dump(),
                                                    background_tasks=background_tasks,
                                                    menu_id=menu_id,
                                                    redis=request.app.state.redis)
    except NoSuchSubmenuError:
        raise HTTPException(status_code=404, detail='submenu not found')

    return submenu


@router.delete('/{menu_id}/submenus/{submenu_id}',
               responses={200: {'description': 'Submenu successfully deleted',
                                'content': {
                                    'application/json': {
                                        'example': {
                                            'detail': 'submenu has been deleted'}
                                    }
                                }}
                          })
async def delete_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         request: Request,
                         background_tasks: BackgroundTasks,
                         service: SubmenuService = Depends(get_submenu_service)) -> dict:
    await service.delete(submenu_id,
                         background_tasks=background_tasks,
                         menu_id=menu_id,
                         redis=request.app.state.redis)

    return {'detail': 'submenu has been deleted'}


# Endpoints for Dish

@router.get('/{menu_id}/submenus/{submenu_id}/dishes', response_model=list[DishRetrieve])
async def get_dishes(menu_id: UUID,
                     submenu_id: UUID,
                     request: Request,
                     background_tasks: BackgroundTasks,
                     service: DishService = Depends(get_dish_service)) -> list[DishRetrieve]:
    dishes = await service.retrieve_list_by_submenu_id(submenu_id,
                                                       background_tasks=background_tasks,
                                                       redis=request.app.state.redis)
    return dishes


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
            response_model=DishRetrieve,
            responses={**DISH_NOT_FOUND})
async def get_dish(menu_id: UUID,
                   submenu_id: UUID,
                   dish_id: UUID,
                   request: Request,
                   background_tasks: BackgroundTasks,
                   service: DishService = Depends(get_dish_service)) -> DishRetrieve:
    try:
        dish = await service.retrieve_one(dish_id,
                                          background_tasks=background_tasks,
                                          redis=request.app.state.redis,
                                          menu_id=menu_id,
                                          submenu_id=submenu_id)
    except NoSuchDishError:
        raise HTTPException(status_code=404, detail='dish not found')

    return dish


@router.post('/{menu_id}/submenus/{submenu_id}/dishes', status_code=201, response_model=DishRetrieve)
async def add_dish(menu_id: UUID,
                   submenu_id: UUID,
                   data: DishCreateUpdate,
                   request: Request,
                   background_tasks: BackgroundTasks,
                   service: DishService = Depends(get_dish_service)) -> DishRetrieve:
    data = data.model_dump()
    data['submenu_id'] = submenu_id

    dish = await service.create_and_retrieve(data,
                                             background_tasks=background_tasks,
                                             redis=request.app.state.redis,
                                             menu_id=menu_id,
                                             submenu_id=submenu_id)

    return dish


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
              response_model=DishRetrieve,
              responses={**DISH_NOT_FOUND}
              )
async def update_dish(menu_id: UUID,
                      submenu_id: UUID,
                      dish_id: UUID,
                      data: DishCreateUpdate,
                      request: Request,
                      background_tasks: BackgroundTasks,
                      service: DishService = Depends(get_dish_service)) -> DishRetrieve:
    try:
        dish = await service.update_and_retrieve(dish_id,
                                                 data.model_dump(),
                                                 background_tasks=background_tasks,
                                                 redis=request.app.state.redis,
                                                 menu_id=menu_id,
                                                 submenu_id=submenu_id)
    except NoSuchDishError:
        raise HTTPException(status_code=404, detail='dish not found')

    return dish


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
               responses={200: {'description': 'Dish successfully deleted',
                                'content': {
                                    'application/json': {
                                        'example': {
                                            'detail': 'dish has been deleted'}
                                    }
                                }}
                          })
async def delete_dish(menu_id: UUID,
                      submenu_id: UUID,
                      dish_id: UUID,
                      request: Request,
                      background_tasks: BackgroundTasks,
                      service: DishService = Depends(get_dish_service)) -> dict:
    await service.delete(dish_id,
                         background_tasks=background_tasks,
                         redis=request.app.state.redis,
                         menu_id=menu_id,
                         submenu_id=submenu_id)

    return {'detail': 'dish has been deleted'}
