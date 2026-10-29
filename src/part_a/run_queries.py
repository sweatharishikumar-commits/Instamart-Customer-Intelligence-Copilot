import sqlite3
import pandas as pd

conn = sqlite3.connect("data/instamart.db")
#QUERY!
query1 = """
SELECT
    customer_id,
    SUM(order_amount) AS total_amount
FROM orders
WHERE status='completed'
AND order_amount > 500
GROUP BY customer_id
HAVING SUM(order_amount) > 8000;
"""
q1 = pd.read_sql_query(query1, conn)
print(q1)
print("Rows:", len(q1))

#QUERY2
q2 = """
SELECT
    c.city,
    p.category,
    ROUND(SUM(o.order_amount),2) AS revenue
FROM orders o
JOIN customers c
ON o.customer_id=c.customer_id
JOIN products p
ON o.product_id=p.product_id
WHERE o.status='completed'
GROUP BY c.city,p.category;
"""
q2_df = pd.read_sql_query(q2, conn)
print("\nQ2")
print("Rows:", len(q2_df))
print(
    "Revenue:",
    round(q2_df["revenue"].sum(),2)
)
#QUERY3
q3 = """
SELECT
    product_name,
    price_inr
FROM products
WHERE price_inr >
(
    SELECT AVG(price_inr)
    FROM products
);
"""
q3_df = pd.read_sql_query(q3, conn)
print("\nQ3")
print("Products:", len(q3_df))
#QUERY4
q4 = """
SELECT
    c.customer_id
FROM customers c
LEFT JOIN
(
    SELECT DISTINCT customer_id
    FROM orders
    WHERE status='completed'
) o
ON c.customer_id=o.customer_id
WHERE o.customer_id IS NULL;
"""
q4_df = pd.read_sql_query(q4, conn)
print("\nQ4")
print("Customers:", len(q4_df))
#QUERY5
q5 = """
WITH customer_spend AS
(
    SELECT
        customer_id,
        SUM(order_amount) total_spend
    FROM orders
    WHERE status='completed'
    GROUP BY customer_id
),
avg_spend AS
(
    SELECT AVG(total_spend) avg_total
    FROM customer_spend
)
SELECT *
FROM customer_spend
WHERE total_spend >
(
    SELECT avg_total
    FROM avg_spend
);
"""
q5_df = pd.read_sql_query(q5, conn)
print("\nQ5")
print("Customers:", len(q5_df))
#QUERY6
q6 = """
WITH customer_totals AS
(
    SELECT
        c.city,
        o.customer_id,
        SUM(o.order_amount) AS total_spend
    FROM orders o
    JOIN customers c
    ON o.customer_id=c.customer_id
    WHERE o.status='completed'
    GROUP BY c.city,o.customer_id
)
SELECT
    city,
    customer_id,
    total_spend,

    RANK() OVER(
        PARTITION BY city
        ORDER BY total_spend DESC
    ) AS rank_no,

    DENSE_RANK() OVER(
        PARTITION BY city
        ORDER BY total_spend DESC
    ) AS dense_rank_no,

    ROW_NUMBER() OVER(
        PARTITION BY city
        ORDER BY total_spend DESC
    ) AS row_number_no
FROM customer_totals;
"""
q6_df = pd.read_sql_query(q6, conn)
print("\nQ6")
print(q6_df.head())
#QUERY7
q7 = """
WITH daily_revenue AS
(
    SELECT
        SUBSTR(order_ts,1,10) day,
        SUM(order_amount) revenue
    FROM orders
    WHERE status='completed'
    GROUP BY day
)
SELECT
    day,
    revenue,
    SUM(revenue)
    OVER(ORDER BY day) cumulative_revenue
FROM daily_revenue;
"""
q7_df = pd.read_sql_query(q7, conn)
print("\nQ7")
print("Rows:", len(q7_df))
print(
    "Final Revenue:",
    round(
        q7_df["cumulative_revenue"].iloc[-1],
        2
    )
)
conn.close()