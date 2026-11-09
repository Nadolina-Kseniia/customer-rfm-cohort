import pandas as pd


def calculate_cohorts(users: pd.DataFrame, txs: pd.DataFrame) -> pd.DataFrame:
    users["signup_month"] = pd.to_datetime(users["signup_date"]).dt.to_period("M")
    txs["tx_month"] = pd.to_datetime(txs["tx_date"]).dt.to_period("M")

    df = txs.merge(users, on="user_id")
    df["cohort_index"] = (df["tx_month"] - df["signup_month"]).apply(lambda x: x.n)

    cohort_data = df.groupby(["signup_month", "cohort_index"])["user_id"].nunique().reset_index()
    cohort_counts = cohort_data.pivot(index="signup_month", columns="cohort_index", values="user_id")

    # ИСПРАВЛЕНИЕ: Берем размер когорты из таблицы users (все зарегистрировавшиеся),
    # а не из первой колонки с транзакциями
    cohort_sizes = users.groupby("signup_month")["user_id"].nunique()

    # Делим на правильный знаменатель и переводим в проценты
    retention = cohort_counts.divide(cohort_sizes, axis=0).round(3) * 100

    # Заменяем пустые значения (NaN) на 0, чтобы график был ровным
    retention = retention.fillna(0)

    return retention