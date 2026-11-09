import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

np.random.seed(42)
N_USERS = 500
N_TXS = 15000
START_DATE = datetime(2025, 1, 1)

# Создаем пользователей (дата регистрации = начало одного из 12 месяцев)
users = pd.DataFrame({
    "user_id": range(1, N_USERS + 1),
    "signup_date": [START_DATE + timedelta(days=np.random.randint(0, 365)) for _ in range(N_USERS)]
})

# Генерируем транзакции
rows = []
for user_id in users["user_id"]:
    signup = users.loc[users["user_id"] == user_id, "signup_date"].values[0]

    # Чем дальше, тем меньше вероятность, что клиент совершит покупку (симуляция оттока)
    for month in range(12):
        tx_date = signup + timedelta(days=month * 30 + np.random.randint(1, 28))
        if tx_date > datetime(2026, 1, 1):
            continue

        # Вероятность транзакции снижается со временем
        prob = max(0.05, 0.9 - (month * 0.1))
        if np.random.rand() < prob:
            # В среднем 1-3 транзакции в месяц
            for _ in range(np.random.randint(1, 4)):
                rows.append({
                    "user_id": user_id,
                    "tx_date": tx_date,
                    "amount": np.random.randint(100, 5000)
                })

txs = pd.DataFrame(rows)
Path("data").mkdir(exist_ok=True)
users.to_csv("data/users.csv", index=False)
txs.to_csv("data/transactions.csv", index=False)
print(f"✔ Сгенерировано {len(users)} клиентов и {len(txs)} транзакций")