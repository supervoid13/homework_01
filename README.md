## Getting Started

### Installation

1. Clone the repo:
  ```sh
  git clone https://github.com/supervoid13/homework_01.git
  ```
2. Create and fill the `.env` in the project root. There is an example in `.env.example` that can help you.

3. Create and activate a virtual environment (from the project root):
##### Linux
  ```sh
  python3 -m venv venv
  ```
  ```sh
  source venv/bin/activate
  ```
##### Windows
  ```sh
  python -m venv venv
  ```
  ```sh
  venv\Scripts\activate
  ```
4. Install packages:
  ```sh
  pip install -r requirements.txt
  ```

5. Start the application:
  ```sh
  uvicorn src.main:app
  ```


### Testing
1. Start containers and wait untill they are on:
  ```sh
  docker-compose up -d
  ```
2. Open a shell in the app container:
  ```sh
  docker exec -it api_container sh
  ```
3. Start tests:
  ```sh
  pytest -s -v
  ```

### Path to single ORM query
/src/menu/crud.py::count_submenus_and_dishes_in_one_request