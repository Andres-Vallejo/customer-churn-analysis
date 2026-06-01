from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "customer_churn.csv"

st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")
st.title("Customer Churn Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["ticket_rate"] = (df["support_tickets"] / df["tenure_months"].clip(lower=1)).round(3)
    df["revenue_at_risk"] = df["monthly_fee"] * df["churned"]
    return df

df = load_data()
segments = st.multiselect("Segment", sorted(df["segment"].unique()), default=sorted(df["segment"].unique()))
contracts = st.multiselect("Contract", sorted(df["contract"].unique()), default=sorted(df["contract"].unique()))
filtered = df[df["segment"].isin(segments) & df["contract"].isin(contracts)]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Customers", len(filtered))
k2.metric("Churn rate", format(filtered['churned'].mean(), ".1%"))
k3.metric("Revenue at risk", "$" + format(filtered['revenue_at_risk'].sum(), ",.0f"))
k4.metric("Avg NPS", format(filtered['nps_score'].mean(), ".1f"))

st.subheader("Segment scorecard")
scorecard = filtered.groupby(["segment", "contract"]).agg(
    customers=("customer_id", "count"),
    churn_rate=("churned", "mean"),
    avg_monthly_fee=("monthly_fee", "mean"),
    avg_nps=("nps_score", "mean"),
    avg_support_tickets=("support_tickets", "mean"),
).round(3).sort_values("churn_rate", ascending=False)
st.dataframe(scorecard, use_container_width=True)

st.subheader("Customer records")
st.dataframe(filtered.sort_values(["churned", "monthly_fee"], ascending=False), use_container_width=True)
