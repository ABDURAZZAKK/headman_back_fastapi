import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


# URLs
# "postgresql://root:root@localhost:5433/HEADMAN_DB"
DATABASE_URL=os.getenv('PG_DATABASE_URL')
TEST_DATABASE_URL=os.getenv('TEST_PG_DATABASE_URL')

# PATHs
HW_ATTACHED_PATH='media\\hw_attached'

# SECURITY
ACCESS_TOKEN_EXPIRE_MINUTES =  int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')


