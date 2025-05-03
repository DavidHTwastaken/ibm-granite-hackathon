import dotenv
import os

dotenv.load_dotenv('.env')

TOKEN = os.getenv('API_TOKEN')