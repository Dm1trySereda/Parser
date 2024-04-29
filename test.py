import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("BROKER_URL"),
      os.getenv("RESULT_BACKEND"),
      os.getenv("MYSQL_HOST"),
      os.getenv("MYSQL_ROOT_PASSWORD"),
      os.getenv("MYSQL_DATABASE"),
      os.getenv("MYSQL_USER"),
      os.getenv("MYSQL_PASSWORD"),
      os.getenv("MYSQL_PORT"))
