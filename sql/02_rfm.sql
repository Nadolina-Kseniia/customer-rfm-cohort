WITH user_stats AS (
    SELECT
        user_id,
        MAX(tx_date) AS last_tx_date,
        COUNT(*) AS frequency,
        SUM(amount) AS monetary
    FROM transactions
    GROUP BY user_id
),
rfm_scores AS (
    SELECT
        user_id,
        last_tx_date,
        frequency,
        monetary,
        -- NTILE(5) делит клиентов на 5 равных групп (1 - худшие, 5 - лучшие)
        NTILE(5) OVER (ORDER BY last_tx_date DESC) AS r_score, -- Чем позже покупка, тем выше R
        NTILE(5) OVER (ORDER BY frequency DESC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary DESC) AS m_score
    FROM user_stats
)
SELECT
    user_id,
    r_score, f_score, m_score,
    (r_score + f_score + m_score) AS total_rfm_score,
    CASE
        WHEN (r_score + f_score + m_score) >= 13 THEN 'VIP / Champions'
        WHEN (r_score + f_score + m_score) >= 10 THEN 'Loyal'
        WHEN (r_score + f_score + m_score) >= 7 THEN 'Potential'
        WHEN (r_score + f_score + m_score) >= 5 THEN 'At Risk'
        ELSE 'Lost'
    END AS segment
FROM rfm_scores
ORDER BY total_rfm_score DESC;