from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_USERNAME = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")


DB_HOST_WAREHOUSE = os.getenv("POSTGRES_HOST_WAREHOUSE")


def connect_db_source():
    engine = create_engine(
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    print(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
    return engine


def connect_db_warehouse():
    engine = create_engine(
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST_WAREHOUSE}/{DB_NAME}"
    )
    print(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST_WAREHOUSE}/{DB_NAME}")
    return engine
