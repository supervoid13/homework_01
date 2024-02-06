import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

DB_PORT_TEST = os.getenv('DB_PORT_TEST')
DB_USER_TEST = os.getenv('DB_USER_TEST')
DB_PASSWORD_TEST = os.getenv('DB_PASSWORD_TEST')
DB_NAME_TEST = os.getenv('DB_NAME_TEST')
