## Getting Started

### Installation

1. Clone the repo:
  ```sh
  git clone https://github.com/supervoid13/homework_01.git
  ```
2. Fill `.env` with your data. (or just rename `.env.example` to `.env` for simplicity)

3. Start containers and wait untill they are on:
  ```sh
  docker-compose up
  ```

### Testing
 Separate container with tests is launched immediately after `docker-compose up`.

### Implementation of Django reverse()
`/src/utils.py::get_url_from_api_route_name`

### OpenAPI specification
`http://localhost:8000/docs`

### Count submenus and dishes with a single ORM query
`/src/menu/crud.py::count_submenus_and_dishes_in_one_request`

### Retrieve menus with all nested entities (point 3)
`/src/menu/crud.py::count_submenus_and_dishes_in_one_request`

### Synchronize data from `/admin/MenuSheets.xlsx` with database (point 5*)
1. Retrieving data from the document: `/src/menu/sheets_parser.py::get_rows`
2. Synchronizing with a database: `/src/menu/tasks_utils.py::synchronize`
3. Celery task: `/src/beat.py::synchronize_from_doc`

### Dish discount (point 6**)
1. Retrieving a dict `discounts` (key - dish_id, value - discount)
2. Current prices are checked directly in the routers.
