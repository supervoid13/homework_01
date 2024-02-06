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
 Separate container with tests is launched immediately after `docker-compose up`. Now you can run Postman tests.
<br>

### Path to the single ORM query
`/src/menu/crud.py::count_submenus_and_dishes_in_one_request`

### OpenAPI specification
`http://localhost:8000/docs`

### Point 6 implementation
`/src/utils.py::get_url_from_api_route_name`
