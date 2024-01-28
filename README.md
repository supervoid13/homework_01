## Getting Started

### Installation

1. Clone the repo:
  ```sh
  git clone https://github.com/supervoid13/homework_01.git
  ```
2. Fill `.env` with your data (`.env.example` could help you)
<br>
3. Start containers and wait untill they are on:
  ```sh
  docker-compose up -d
  ```

### Testing
1. Open a shell in the app container:
  ```sh
  docker exec -it api_container sh
  ```
2. Start tests:
  ```sh
  pytest -s -v
  ```

### Path to the single ORM query
/src/menu/crud.py::count_submenus_and_dishes_in_one_request