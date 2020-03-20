import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')
JIRA_URL = os.getenv('JIRA_URL')

db_connection_test = {
    "host": os.getenv("PCR_DB_HOST"),
    "dbname": os.getenv("PCR_DB_NAME"),
    "user": os.getenv("PCR_DB_USERNAME"),
    "password": os.getenv("PCR_DB_PASSWORD"),
    "port": os.getenv("PCR_DB_PORT"),
    "engine": os.getenv("PCR_DB_ENGINE")
}

db_connection_test1 = {
    "host": os.getenv("PCR_DB_HOST_TEST1"),
    "dbname": os.getenv("PCR_DB_NAME_TEST1"),
    "user": os.getenv("PCR_DB_USERNAME_TEST1"),
    "password": os.getenv("PCR_DB_PASSWORD_TEST1"),
    "port": os.getenv("PCR_DB_PORT_TEST1"),
    "engine": os.getenv("PCR_DB_ENGINE_TEST1")
}

db_connection_dev = {
    "host": os.getenv("PCR_DB_HOST_DEV"),
    "dbname": os.getenv("PCR_DB_NAME_DEV"),
    "user": os.getenv("PCR_DB_USERNAME_DEV"),
    "password": os.getenv("PCR_DB_PASSWORD_DEV"),
    "port": os.getenv("PCR_DB_PORT_DEV"),
    "engine": os.getenv("PCR_DB_ENGINE_DEV")
}

PCR_URL_SHOP = os.getenv('PCR_URL_SHOP')
PCR_URL_TEST1 = os.getenv('PCR_URL_TEST1')
