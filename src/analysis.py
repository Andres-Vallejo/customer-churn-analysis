from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "customer_churn.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["ticket_rate"] = (df["support_tickets"] / df["tenure_months"].clip(lower=1)).round(3)
    df["low_usage_flag"] = (df["usage_hours"] < df["usage_hours"].median()).astype(int)
    df["inactive_flag"] = (df["last_login_days"] >= 14).astype(int)
    df["revenue_at_risk"] = df["monthly_fee"] * df["churned"]
    return df

def train_model(df: pd.DataFrame):
    features = ["segment", "contract", "tenure_months", "monthly_fee", "support_tickets", "nps_score", "usage_hours", "last_login_days", "discount_pct", "ticket_rate", "low_usage_flag", "inactive_flag"]
    X = df[features]
    y = df["churned"]
    categorical = ["segment", "contract"]
    numeric = [c for c in features if c not in categorical]
    preprocessor = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), categorical), ("num", StandardScaler(), numeric)])
    model = Pipeline([("prep", preprocessor), ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    model.fit(X_train, y_train)
    proba = model.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)
    metrics = pd.DataFrame({"metric": ["accuracy", "precision", "recall", "roc_auc"], "value": [round(accuracy_score(y_test, pred), 3), round(precision_score(y_test, pred, zero_division=0), 3), round(recall_score(y_test, pred, zero_division=0), 3), round(roc_auc_score(y_test, proba), 3)]})
    return model, metrics, features

def make_outputs(df: pd.DataFrame, model, metrics: pd.DataFrame, features: list[str]) -> None:
    segment = df.groupby(["segment", "contract"]).agg(customers=("customer_id", "count"), churn_rate=("churned", "mean"), avg_monthly_fee=("monthly_fee", "mean"), avg_nps=("nps_score", "mean"), avg_support_tickets=("support_tickets", "mean")).round(3).reset_index().sort_values("churn_rate", ascending=False)
    segment.to_csv(OUT / "segment_churn_scorecard.csv", index=False)
    metrics.to_csv(OUT / "model_metrics.csv", index=False)
    scored = df.copy()
    scored["churn_risk_score"] = model.predict_proba(scored[features])[:, 1].round(3)
    scored["risk_band"] = pd.cut(scored["churn_risk_score"], bins=[0, 0.35, 0.65, 1], labels=["low", "medium", "high"], include_lowest=True)
    scored["retention_priority"] = (scored["churn_risk_score"] * scored["monthly_fee"]).round(2)
    scored.sort_values("retention_priority", ascending=False).to_csv(OUT / "customer_risk_watchlist.csv", index=False)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=segment, x="churn_rate", y="segment", hue="contract")
    plt.title("Churn rate by segment and contract")
    plt.tight_layout()
    plt.savefig(OUT / "churn_rate_by_segment.png", dpi=160)

def main() -> None:
    df = load_data()
    model, metrics, features = train_model(df)
    make_outputs(df, model, metrics, features)
    print("Premium churn analysis complete.")
    print(metrics)

if __name__ == "__main__":
    main()
