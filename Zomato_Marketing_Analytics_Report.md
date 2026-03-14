# Zomato Marketing Analytics Report

Date: March 14, 2026  
Prepared for: Brand Wars Case Submission

## 1) Problem Statement (PS)

Zomato operates in a highly competitive food delivery market where customer acquisition costs are rising, repeat order rates are plateauing, and marketing ROI is inconsistent across cities and user segments.

Despite running multiple campaigns (discounts, free delivery, influencer marketing, push notifications, and Zomato Gold promotions), the company struggles to identify which marketing levers truly drive long-term customer value.

As a Marketing Analytics Consultant, we are provided with 10,000 rows of customer-level and campaign-level data. The task is to analyze user behavior, campaign performance, and ordering patterns to help Zomato optimize marketing spend and improve customer lifetime value (CLV).

### Business Objectives
1. Identify high-value customer segments.
2. Measure marketing campaign effectiveness.
3. Understand factors influencing repeat orders.
4. Optimize discount and coupon strategies.
5. Improve customer retention and profitability.

### Judging Criteria Alignment
1. Creativity and Originality (25%): unique growth ideas and non-generic strategy design.
2. Market Fit and Customer Insight (30%): strong segmentation and customer behavior understanding.
3. Strategic Coherence and Feasibility: practical implementation roadmap with measurable KPIs.

---

## 2) Dataset Overview

Rows: 10,000 interaction/order records  
Unique customers: 9,943  
Source file: zomato dataset.xlsx

### Column Groups

#### Customer Information
- customer id
- age
- gender
- city
- zomato gold member

#### Order and Behavior Metrics
- order id
- cuisine type
- order value
- discount amount
- payment mode
- delivery time mins

#### Marketing and Campaign Data
- campaign type
- channel
- coupon used
- impressions
- clicks
- conversion flag

#### Loyalty and Retention
- repeat customer
- orders last 30 days
- avg order value
- churn risk score

---

## 3) Analytics Approach

The analysis was designed as a growth-and-retention operating system rather than a one-time KPI pull.

### Step A: Data Standardization
- Renamed columns into snake_case for robust reproducible analysis.
- Converted all numeric fields to proper numeric types.
- Engineered helper variables:
  - repeat_flag (1/0)
  - coupon_used_flag (1/0)
  - discount_ratio = discount_amount / order_value
  - net_order_value = order_value - discount_amount
  - value_segment from orders_last_30_days:
    - Low Value: 0 to 3 orders
    - Mid Value: 4 to 7 orders
    - High Value: 8+ orders

### Step B: KPI Tables
Generated five KPI outputs:
1. overall.csv
2. high_value_segments.csv
3. campaign_perf.csv
4. discount_eff.csv
5. retention_matrix.csv

### Step C: Repeat-Order Driver Model
- Target variable: repeat_flag
- Model: Logistic Regression with categorical one-hot encoding and standardized numerical inputs
- Split: 75/25 stratified train-test
- Output:
  - repeat_model_metrics.txt
  - repeat_model_feature_importance.csv

---

## 4) Key Results (Detailed)

## 4.1 Overall Business Health

From overall.csv:

- Customers: 9,943
- Orders: 10,000
- GMV: 6,784,098.92
- Discounts: 1,513,587.23
- Net value after discounts: 5,270,511.69
- Repeat rate: 56.05%
- Average churn risk score: 49.36

Derived metric:
- Discount-to-GMV ratio = 1,513,587.23 / 6,784,098.92 = 22.31%

Interpretation:
- Repeat rate is moderate, but discount spend is high.
- Current growth appears discount-supported, which risks margin compression if not optimized.

## 4.2 Campaign Performance Analysis

Top campaign-channel combinations by conversion volume:
1. Paid Ads + Email: 406 conversions
2. Email + Email: 381 conversions
3. Influencer + Email: 380 conversions
4. Paid Ads + Instagram: 376 conversions
5. Email + Google: 373 conversions

Best combinations by repeat quality (among combinations with strong conversion scale):
1. Influencer + Google: repeat rate 58.09%
2. Push Notification + Instagram: repeat rate 58.09%
3. Influencer + Instagram: repeat rate 58.08%
4. Email + App Push: repeat rate 57.12%
5. Email + Email: repeat rate 56.51%

Interpretation:
- Conversion volume winners are not always retention-quality winners.
- Marketing budget should be split by objective:
  - Acquisition volume engine: Paid Ads + Email
  - Retention-quality engine: Influencer + Google, Push + Instagram

## 4.3 High-Value Segment Insights by City

Top city-value combinations by average AOV:
1. Bangalore Mid Value: AOV 571.28, repeat 58.35%
2. Chennai High Value: AOV 563.31, repeat 56.04%
3. Chennai Mid Value: AOV 563.01, repeat 56.66%
4. Delhi High Value: AOV 561.23, repeat 56.74%
5. Mumbai High Value: AOV 560.17, repeat 55.05%

Interpretation:
- Mid-value users in some cities are equally monetizable as high-value users.
- This supports city-specific growth design instead of one nationwide campaign template.

## 4.4 Discount and Coupon Efficiency

From discount_eff.csv:

- Low Value with coupon:
  - Conversion rate 62.52% (higher than no-coupon 58.36%)
  - Repeat rate 57.51% (higher than no-coupon 55.44%)

- Mid Value with coupon:
  - Conversion rate 60.57% (higher than no-coupon 56.94%)
  - Repeat rate 55.08% (lower than no-coupon 57.81%)

- High Value with coupon:
  - Conversion rate nearly unchanged (~59.58% both)
  - Repeat rate lower with coupon (55.04%) vs no-coupon (56.65%)

Interpretation:
- Couponing works best for Low Value activation.
- For Mid and High Value, broad coupons may create discount dependency and reduce repeat quality.
- Segment-led coupon controls are required to protect profitability.

## 4.5 Retention Risk Matrix

High-risk cohort sizes:
- High Risk + High Value: 1,299 customers
- High Risk + Mid Value: 797 customers
- High Risk + Low Value: 636 customers

Interpretation:
- Most important save segment is High Risk + High Value.
- This cohort has the largest strategic downside if churned and should be the first retention priority.

## 4.6 Repeat Model Findings

Model quality from repeat_model_metrics.txt:
- ROC-AUC: 0.4993
- Accuracy: ~50%

Interpretation:
- Predictive signal for repeat behavior is weak in current variables.
- This is a valuable finding: decisions should rely more on controlled experiments and incremental lift testing than pure predictive targeting.

Top model coefficients (directional, not causal):
- Positive: cuisine_type_South Indian, city_Bangalore, payment_mode_UPI
- Negative: cuisine_type_Desserts, city_Mumbai, city_Hyderabad

Model caveat:
- Since model performance is near random, these coefficients should be used as exploratory signals only.

---

## 5) Strategic Recommendations

## 5.1 Budget Architecture
Create a two-pool budget framework:
1. Acquisition Pool (volume): prioritize Paid Ads + Email.
2. Retention-Quality Pool: prioritize Influencer + Google and Push + Instagram.

## 5.2 Segment-Wise Discount Strategy
1. Low Value:
- Use tactical coupons for first-to-second-order conversion.
- Time-box coupon validity (24 to 72 hours).

2. Mid Value:
- Use conditional offers (minimum order value, capped discount).
- Shift from pure price incentives to convenience nudges.

3. High Value:
- Reduce blanket coupons.
- Offer non-price loyalty benefits (priority delivery windows, premium support, curated cuisine access).

## 5.3 Retention Prioritization
Priority ladder:
1. High Risk + High Value
2. High Risk + Mid Value
3. Medium Risk + High Value

Playbook:
- Triggered win-back journeys.
- Service reliability interventions for delayed delivery users.
- Personalized channel and cuisine recommendations.

## 5.4 Experimentation Framework
Run controlled experiments every cycle:
1. A/B Test: targeted vs blanket coupons.
2. Geo holdout: city-level channel mix tests.
3. Timing tests: meal-window push vs fixed-time push.

Primary success metrics:
- Incremental repeat rate
- Net contribution after discount
- 60/90-day retention

---

## 6) 90-Day Implementation Plan

### Days 0-30
1. Deploy KPI dashboard from generated tables.
2. Freeze bottom-decile campaign combinations by ROI proxy.
3. Launch Low Value reactivation coupon test.

### Days 31-60
1. Apply segment-based discount guardrails.
2. Launch high-risk retention journeys.
3. Start city-level channel reallocation pilot.

### Days 61-90
1. Institutionalize monthly marketing mix rebalancing.
2. Move to CLV-weighted campaign scorecard.
3. Scale proven experiments nationally.

---

## 7) How to Reproduce the Analysis

## 7.1 Python Execution
Run:

```powershell
python marketing_kpis.py
```

This creates:
- outputs/overall.csv
- outputs/high_value_segments.csv
- outputs/campaign_perf.csv
- outputs/discount_eff.csv
- outputs/retention_matrix.csv
- outputs/repeat_model_feature_importance.csv
- outputs/repeat_model_metrics.txt

## 7.2 SQL Usage
Load data into a table named zomato_raw with original column names, then execute the SQL in the appendix.

---

## 8) Appendix A: Full SQL Code

```sql
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
```

---

## 9) Appendix B: Full Python Code

```python
"""Zomato Marketing Analytics KPI Pack (Python)

What this script does:
1) Reads the Excel dataset
2) Standardizes columns
3) Computes KPI tables aligned to business objectives
4) Builds a simple repeat-order model and feature importances
5) Exports outputs to CSV for your presentation
"""

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DATA_FILE = Path("zomato dataset.xlsx")
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path)

    # Normalize columns to snake_case for coding convenience.
    rename_map = {
        "customer id": "customer_id",
        "age": "age",
        "gender": "gender",
        "city": "city",
        "zomato gold member": "gold_member",
        "order id": "order_id",
        "order value": "order_value",
        "discount amount": "discount_amount",
        "payment mode": "payment_mode",
        "delivery time mins": "delivery_time_mins",
        "cuisine type": "cuisine_type",
        "campaign type": "campaign_type",
        "channel": "channel",
        "coupon used": "coupon_used",
        "impressions": "impressions",
        "clicks": "clicks",
        "conversion flag": "conversion_flag",
        "repeat customer": "repeat_customer",
        "orders last 30 days": "orders_last_30_days",
        "avg order value": "avg_order_value",
        "churn risk score": "churn_risk_score",
    }
    df = df.rename(columns=rename_map)

    # Type cleanup.
    num_cols = [
        "age",
        "order_value",
        "discount_amount",
        "delivery_time_mins",
        "impressions",
        "clicks",
        "conversion_flag",
        "orders_last_30_days",
        "avg_order_value",
        "churn_risk_score",
    ]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df["gold_member_flag"] = (df["gold_member"].str.lower() == "yes").astype(int)
    df["coupon_used_flag"] = (df["coupon_used"].str.lower() == "yes").astype(int)
    df["repeat_flag"] = (df["repeat_customer"].str.lower() == "yes").astype(int)

    df["discount_ratio"] = (df["discount_amount"] / df["order_value"]).fillna(0)
    df["net_order_value"] = df["order_value"] - df["discount_amount"]

    df["value_segment"] = pd.cut(
        df["orders_last_30_days"],
        bins=[-1, 3, 7, float("inf")],
        labels=["Low Value", "Mid Value", "High Value"],
    )
    return df


def build_kpi_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    overall = pd.DataFrame(
        {
            "customers": [df["customer_id"].nunique()],
            "orders": [df["order_id"].nunique()],
            "gmv": [df["order_value"].sum()],
            "discounts": [df["discount_amount"].sum()],
            "nmv_after_discount": [df["net_order_value"].sum()],
            "repeat_rate": [df["repeat_flag"].mean()],
            "avg_churn_risk": [df["churn_risk_score"].mean()],
        }
    )

    high_value_segments = (
        df.groupby(["city", "value_segment"], observed=False)
        .agg(
            customers=("customer_id", "nunique"),
            avg_aov=("avg_order_value", "mean"),
            avg_orders_30d=("orders_last_30_days", "mean"),
            repeat_rate=("repeat_flag", "mean"),
            avg_churn_risk=("churn_risk_score", "mean"),
        )
        .reset_index()
    )

    campaign_perf = (
        df.groupby(["campaign_type", "channel"], observed=False)
        .agg(
            impressions=("impressions", "sum"),
            clicks=("clicks", "sum"),
            conversions=("conversion_flag", "sum"),
            avg_order_value=("order_value", "mean"),
            repeat_rate=("repeat_flag", "mean"),
            avg_churn_risk=("churn_risk_score", "mean"),
        )
        .reset_index()
    )
    campaign_perf["ctr"] = campaign_perf["clicks"] / campaign_perf["impressions"].clip(lower=1)
    campaign_perf["cvr"] = campaign_perf["conversions"] / campaign_perf["clicks"].clip(lower=1)

    discount_eff = (
        df.groupby(["value_segment", "coupon_used"], observed=False)
        .agg(
            rows_count=("order_id", "count"),
            avg_discount_ratio=("discount_ratio", "mean"),
            conversion_rate=("conversion_flag", "mean"),
            repeat_rate=("repeat_flag", "mean"),
            avg_net_order_value=("net_order_value", "mean"),
        )
        .reset_index()
    )

    retention_matrix = df.copy()
    retention_matrix["risk_bucket"] = pd.cut(
        retention_matrix["churn_risk_score"],
        bins=[-1, 39, 69, 100],
        labels=["Low Risk", "Medium Risk", "High Risk"],
    )
    retention_matrix = (
        retention_matrix.groupby(["risk_bucket", "value_segment"], observed=False)
        .agg(
            customers=("customer_id", "nunique"),
            repeat_rate=("repeat_flag", "mean"),
            avg_orders_30d=("orders_last_30_days", "mean"),
            avg_aov=("avg_order_value", "mean"),
        )
        .reset_index()
    )

    return {
        "overall": overall,
        "high_value_segments": high_value_segments,
        "campaign_perf": campaign_perf,
        "discount_eff": discount_eff,
        "retention_matrix": retention_matrix,
    }


def repeat_model(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    features = [
        "age",
        "city",
        "gold_member",
        "order_value",
        "discount_amount",
        "delivery_time_mins",
        "payment_mode",
        "cuisine_type",
        "campaign_type",
        "channel",
        "coupon_used",
        "orders_last_30_days",
        "avg_order_value",
        "churn_risk_score",
    ]
    target = "repeat_flag"

    model_df = df[features + [target]].dropna(subset=[target]).copy()

    X = model_df[features]
    y = model_df[target]

    numeric_features = [
        "age",
        "order_value",
        "discount_amount",
        "delivery_time_mins",
        "orders_last_30_days",
        "avg_order_value",
        "churn_risk_score",
    ]
    categorical_features = [c for c in features if c not in numeric_features]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )

    clf = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    clf.fit(X_train, y_train)
    probs = clf.predict_proba(X_test)[:, 1]
    preds = clf.predict(X_test)

    auc = roc_auc_score(y_test, probs)
    report = classification_report(y_test, preds)

    onehot = clf.named_steps["preprocess"].named_transformers_["cat"].named_steps["onehot"]
    feature_names = numeric_features + list(onehot.get_feature_names_out(categorical_features))
    coeffs = clf.named_steps["model"].coef_[0]

    importance = pd.DataFrame({"feature": feature_names, "coefficient": coeffs})
    importance["abs_coeff"] = importance["coefficient"].abs()
    importance = importance.sort_values("abs_coeff", ascending=False).drop(columns=["abs_coeff"])

    metrics_text = f"ROC-AUC: {auc:.4f}\n\nClassification Report:\n{report}"
    return importance, metrics_text


def main() -> None:
    df = load_data(DATA_FILE)

    kpis = build_kpi_tables(df)
    for name, table in kpis.items():
        table.to_csv(OUT_DIR / f"{name}.csv", index=False)

    importance, metrics_text = repeat_model(df)
    importance.to_csv(OUT_DIR / "repeat_model_feature_importance.csv", index=False)
    (OUT_DIR / "repeat_model_metrics.txt").write_text(metrics_text, encoding="utf-8")

    print("KPI pack generated in ./outputs")
    print("Files created:")
    for p in sorted(OUT_DIR.glob("*")):
        print(f"- {p.name}")


if __name__ == "__main__":
    main()
```

---

## 10) Conclusion

This analysis indicates that Zomato can improve growth quality by moving from broad discount-led execution to segment-led, city-aware, and retention-prioritized marketing.

Core takeaway:
- Keep scale where conversion is strong.
- Shift spend toward campaign combinations with stronger repeat quality.
- Protect margin through selective couponing.
- Prioritize high-risk high-value customer save programs.
- Use experimentation as the primary optimization engine when predictive model signal is weak.
