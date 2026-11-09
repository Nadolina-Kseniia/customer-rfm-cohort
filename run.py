import pandas as pd
from src.db import get_engine, load_data
from src.analysis import calculate_cohorts
from src.report import save_cohort_heatmap


def main():
    engine = get_engine()
    users, txs = load_data(engine)

    # Выполняем SQL для RFM и сохраняем результат
    rfm_df = pd.read_sql(
        "SELECT * FROM (SELECT user_id, last_tx_date, frequency, monetary, NTILE(5) OVER (ORDER BY last_tx_date DESC) AS r_score, NTILE(5) OVER (ORDER BY frequency DESC) AS f_score, NTILE(5) OVER (ORDER BY monetary DESC) AS m_score FROM (SELECT user_id, MAX(tx_date) AS last_tx_date, COUNT(*) AS frequency, SUM(amount) AS monetary FROM transactions GROUP BY user_id) AS stats) AS rfm;",
        engine)
    rfm_df.to_csv("outputs/rfm_segments.csv", index=False)

    # Считаем когорты и рисуем график
    retention = calculate_cohorts(users, txs)
    save_cohort_heatmap(retention)
    print("✔ Анализ завершен. Результаты в папке outputs/")


if __name__ == "__main__":
    main()