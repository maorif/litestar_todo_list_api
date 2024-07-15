import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", default="")
POSTGRES_PSWD = os.getenv("POSTGRES_PSWD", default="")
POSTGRES_USER = os.getenv("POSTGRES_USER", default="")
POSTGRES_DB = os.getenv("POSTGRES_DB", default="")
