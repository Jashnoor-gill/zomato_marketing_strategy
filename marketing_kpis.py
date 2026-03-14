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
