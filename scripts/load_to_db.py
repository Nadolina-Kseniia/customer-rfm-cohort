import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Подключаемся к базе rfm_db на порту 5434
engine = create_engine(
    os.getenv("DB_URL", "postgresql+psycopg2://postgres:postgres@localhost:5434/rfm_db")
)

def load_csv_to_db():
    # Указываем пути к файлам
    users_path = Path("data/users.csv")
    txs_path = Path("data/transactions.csv")

    if not users_path.exists() or not txs_path.exists():
        print("❌ Ошибка: CSV-файлы не найдены. Запустите сначала python data/generate_data.py")
        return

    print("⏳ Читаем CSV-файлы...")
    # parse_dates нужен, чтобы даты корректно записались в PostgreSQL (как TIMESTAMP)
    users = pd.read_csv(users_path, parse_dates=["signup_date"])
    txs = pd.read_csv(txs_path, parse_dates=["tx_date"])

    print("⏳ Загружаем данные в PostgreSQL...")
    # if_exists="append" добавляет данные в уже созданные таблицы
    users.to_sql("users", engine, if_exists="append", index=False)
    txs.to_sql("transactions", engine, if_exists="append", index=False)

    print(f"✔ Успешно загружено: {len(users)} клиентов и {len(txs)} транзакций!")

if __name__ == "__main__":
    load_csv_to_db()