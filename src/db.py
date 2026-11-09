import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    # Дефолтный URL на случай, если .env не подхватится
    url = os.getenv("DB_URL", "postgresql+psycopg2://postgres:postgres@localhost:5434/rfm_db")
    return create_engine(url)

def load_data(engine):
    # Загружаем обе таблицы
    users = pd.read_sql("SELECT * FROM users", engine)
    txs = pd.read_sql("SELECT * FROM transactions", engine)
    return users, txs