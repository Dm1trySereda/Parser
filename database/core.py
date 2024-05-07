import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import URL

load_dotenv()

db_connection_url = URL.create(
    "mysql+pymysql",
    username=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host="localhost",
    port=os.getenv("MYSQL_PORT"),
    database=os.getenv("MYSQL_DATABASE"),
)
engine = create_engine(db_connection_url)

async_db_connection_url = URL.create(
    "mysql+aiomysql",
    username=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=os.getenv("MYSQL_PORT"),
    database=os.getenv("MYSQL_DATABASE"),

)

async_engine = create_async_engine(async_db_connection_url)
