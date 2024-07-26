import os
from dotenv import load_dotenv

load_dotenv()

API_ID: int = os.getenv('API_ID') 
API_HASH: str = os.getenv('API_HASH')
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
LIST_OF_ADMINS: list[int] = [int(user_id) for user_id in os.getenv('SUDO').split()]
DST_ID: int= int(os.getenv('DUMP_ID'))




if __name__ == "__main__":
    print(DST_ID)
    print(type(-1))
