import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

# POSTGRES
PG_USER = os.getenv('POSTGRES_USER')
PG_PASS = os.getenv('POSTGRES_PASSWORD')
PG_HOST = os.getenv('POSTGRES_HOST')
PG_PORT = os.getenv('POSTGRES_PORT')
PG_DB = os.getenv('POSTGRES_DB')

# URLs
# "postgresql://root:root@localhost:5433/HEADMAN_DB"
DATABASE_URL=f"postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

# PATHs
HW_ATTACHED_PATH='media\\hw_attached'

# SECURITY
ACCESS_TOKEN_EXPIRE_MINUTES =  int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')


