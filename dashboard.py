from pathlib import Path

import pandas as pd
import streamlit as st

from src.risk_engine import score_dataframe


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_FILE = PROJECT_ROOT / "data" / "transactions.csv"


st.set_page_config(
    page_title="Risk Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Risk Monitoring Dashboard")
st.caption(
    "Synthetic portfolio project — explainable transaction risk scoring."
)

if not DATA_FILE.exists():
    st.error(
        "Synthetic data not found. Run `python -m src.generate_data` first."
    )
    st.stop()

dataframe = pd.read_csv(DATA_FILE)
scored = score_dataframe(dataframe)

risk_options = ["All", "Low", "Medium", "High", "Critical"]
selected_level = st.sidebar.selectbox("Risk level", risk_options)

if selected_level == "All":
    filtered = scored
else:
    filtered = scored[scored["risk_level"] == selected_level]

total_transactions = len(scored)
high_critical = scored["risk_level"].isin(["High", "Critical"]).sum()
critical_count = (scored["risk_level"] == "Critical").sum()
total_value = scored["amount"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Transactions", f"{total_transactions:,}")
col2.metric("High/Critical Alerts", f"{high_critical:,}")
col3.metric("Critical Alerts", f"{critical_count:,}")
col4.metric("Transaction Value", f"₹{total_value:,.0f}")

st.subheader("Risk distribution")

risk_distribution = (
    scored["risk_level"]
    .value_counts()
    .reindex(["Low", "Medium", "High", "Critical"], fill_value=0)
)

st.bar_chart(risk_distribution)

st.subheader("Top alerts")

top_alerts = (
    filtered.sort_values(
        ["risk_score", "amount"],
        ascending=[False, False],
    )
    .head(100)
)

columns_to_show = [
    "transaction_id",
    "customer_id",
    "timestamp",
    "amount",
    "country",
    "channel",
    "kyc_risk",
    "risk_score",
    "risk_level",
    "risk_reasons",
]

st.dataframe(
    top_alerts[columns_to_show],
    use_container_width=True,
    hide_index=True,
)

st.subheader("Risk level by channel")

channel_summary = (
    scored.groupby(["channel", "risk_level"])
    .size()
    .unstack(fill_value=0)
)

for column in ["Low", "Medium", "High", "Critical"]:
    if column not in channel_summary.columns:
        channel_summary[column] = 0

channel_summary = channel_summary[
    ["Low", "Medium", "High", "Critical"]
]

st.bar_chart(channel_summary)
