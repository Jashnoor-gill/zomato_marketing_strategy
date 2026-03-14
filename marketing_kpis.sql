-- Zomato Marketing Analytics KPI SQL Pack
-- Assumption: raw table name is zomato_raw and columns match the Excel header exactly.
-- Dialect: ANSI-style SQL (works with small adjustments in Postgres, DuckDB, Snowflake, BigQuery).

WITH base AS (
    SELECT
        CAST("customer id" AS BIGINT) AS customer_id,
        CAST(age AS INT) AS age,
        gender,
        city,
        "zomato gold member" AS gold_member,
        CAST("order id" AS BIGINT) AS order_id,
        CAST("order value" AS DECIMAL(12,2)) AS order_value,
        CAST("discount amount" AS DECIMAL(12,2)) AS discount_amount,
        "payment mode" AS payment_mode,
        CAST("delivery time mins" AS INT) AS delivery_time_mins,
        "cuisine type" AS cuisine_type,
        "campaign type" AS campaign_type,
        channel,
        "coupon used" AS coupon_used,
        CAST(impressions AS BIGINT) AS impressions,
        CAST(clicks AS BIGINT) AS clicks,
        CAST("conversion flag" AS INT) AS conversion_flag,
        "repeat customer" AS repeat_customer,
        CAST("orders last 30 days" AS INT) AS orders_last_30_days,
        CAST("avg order value" AS DECIMAL(12,2)) AS avg_order_value,
        CAST("churn risk score" AS INT) AS churn_risk_score
    FROM zomato_raw
),
metrics AS (
    SELECT
        *,
        CASE WHEN impressions > 0 THEN 1.0 * clicks / impressions ELSE 0 END AS ctr,
        CASE WHEN clicks > 0 THEN 1.0 * conversion_flag / clicks ELSE 0 END AS cvr_per_row,
        CASE WHEN order_value > 0 THEN 1.0 * discount_amount / order_value ELSE 0 END AS discount_ratio,
        (order_value - discount_amount) AS net_order_value,
        CASE WHEN churn_risk_score >= 70 THEN 1 ELSE 0 END AS high_churn_risk,
        CASE
            WHEN orders_last_30_days >= 8 OR avg_order_value >= 600 THEN 'High Value'
            WHEN orders_last_30_days BETWEEN 4 AND 7 THEN 'Mid Value'
            ELSE 'Low Value'
        END AS value_segment
    FROM base
)

-- 1) Overall business dashboard
SELECT
    COUNT(*) AS rows_count,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(DISTINCT order_id) AS orders,
    SUM(order_value) AS gmv,
    SUM(discount_amount) AS total_discounts,
    SUM(net_order_value) AS nmv_after_discount,
    AVG(delivery_time_mins) AS avg_delivery_time,
    AVG(CASE WHEN repeat_customer = 'Yes' THEN 1.0 ELSE 0 END) AS repeat_rate,
    AVG(churn_risk_score) AS avg_churn_risk
FROM metrics;

-- 2) High-value segment discovery
SELECT
    city,
    value_segment,
    COUNT(DISTINCT customer_id) AS customers,
    AVG(avg_order_value) AS avg_aov,
    AVG(orders_last_30_days) AS avg_order_freq_30d,
    AVG(CASE WHEN repeat_customer = 'Yes' THEN 1.0 ELSE 0 END) AS repeat_rate,
    AVG(churn_risk_score) AS avg_churn_risk
FROM metrics
GROUP BY city, value_segment
ORDER BY city, avg_aov DESC;

-- 3) Campaign effectiveness (funnel + quality)
SELECT
    campaign_type,
    channel,
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(conversion_flag) AS conversions,
    CASE WHEN SUM(impressions) > 0 THEN 1.0 * SUM(clicks) / SUM(impressions) ELSE 0 END AS ctr,
    CASE WHEN SUM(clicks) > 0 THEN 1.0 * SUM(conversion_flag) / SUM(clicks) ELSE 0 END AS cvr,
    AVG(order_value) AS avg_order_value,
    AVG(CASE WHEN repeat_customer = 'Yes' THEN 1.0 ELSE 0 END) AS repeat_rate,
    AVG(churn_risk_score) AS avg_churn_risk
FROM metrics
GROUP BY campaign_type, channel
ORDER BY conversions DESC;

-- 4) Discount efficiency by segment
SELECT
    value_segment,
    coupon_used,
    COUNT(*) AS rows_count,
    AVG(discount_ratio) AS avg_discount_ratio,
    AVG(CASE WHEN conversion_flag = 1 THEN 1.0 ELSE 0 END) AS conversion_rate,
    AVG(CASE WHEN repeat_customer = 'Yes' THEN 1.0 ELSE 0 END) AS repeat_rate,
    AVG(net_order_value) AS avg_net_order_value
FROM metrics
GROUP BY value_segment, coupon_used
ORDER BY value_segment, avg_net_order_value DESC;

-- 5) Repeat-order drivers quick diagnostic
SELECT
    city,
    campaign_type,
    AVG(delivery_time_mins) AS avg_delivery_time,
    AVG(discount_ratio) AS avg_discount_ratio,
    AVG(CASE WHEN repeat_customer = 'Yes' THEN 1.0 ELSE 0 END) AS repeat_rate,
    AVG(churn_risk_score) AS avg_churn_risk
FROM metrics
GROUP BY city, campaign_type
ORDER BY repeat_rate DESC;

-- 6) Retention risk matrix
SELECT
    CASE
        WHEN churn_risk_score >= 70 THEN 'High Risk'
        WHEN churn_risk_score BETWEEN 40 AND 69 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_bucket,
    value_segment,
    COUNT(DISTINCT customer_id) AS customers,
    AVG(CASE WHEN repeat_customer = 'Yes' THEN 1.0 ELSE 0 END) AS repeat_rate,
    AVG(orders_last_30_days) AS avg_orders_30d,
    AVG(avg_order_value) AS avg_aov
FROM metrics
GROUP BY risk_bucket, value_segment
ORDER BY risk_bucket, value_segment;
