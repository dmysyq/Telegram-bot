import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

def create_connection():
    db_path = os.getenv('DB_PATH')
    conn_str = fr'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};'
    return pyodbc.connect(conn_str)
    