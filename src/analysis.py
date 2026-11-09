import pandas as pd


def calculate_cohorts(users: pd.DataFrame, txs: pd.DataFrame) -> pd.DataFrame:
    users["signup_month"] = pd.to_datetime(users["signup_date"]).dt.to_period("M")
    txs["tx_month"] = pd.to_datetime(txs["tx_date"]).dt.to_period("M")

    # merge
    df = txs.merge(users, on="user_id")

    # Вычисляем "возраст" клиента в месяцах (Cohort Index)
    df["cohort_index"] = (df["tx_month"] - df["signup_month"]).apply(lambda x: x.n)

    # Группируем и считаем уникальных пользователей
    cohort_data = df.groupby(["signup_month", "cohort_index"])["user_id"].nunique().reset_index()

    # Считаем Retention (процент вернувшихся)
    cohort_counts = cohort_data.pivot(index="signup_month", columns="cohort_index", values="user_id")
    cohort_sizes = cohort_counts.iloc[:, 0]
    retention = cohort_counts.divide(cohort_sizes, axis=0).round(3) * 100

    return retention