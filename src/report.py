import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def save_cohort_heatmap(retention: pd.DataFrame):
    plt.figure(figsize=(12, 8))
    # Рисуем тепловую карту
    sns.heatmap(retention, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={'label': 'Retention (%)'})
    plt.title("Cohort Retention (Удержание клиентов по месяцам)")
    plt.xlabel("Месяцы с момента регистрации (Cohort Index)")
    plt.ylabel("Месяц регистрации")
    plt.tight_layout()
    plt.savefig("outputs/cohort_heatmap.png", dpi=120)
    print("✔ Тепловая карта сохранена в outputs/cohort_heatmap.png")