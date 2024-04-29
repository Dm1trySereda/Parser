import os
from mysql.connector import connect
from dotenv import load_dotenv

load_dotenv()

db_connection = connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)
