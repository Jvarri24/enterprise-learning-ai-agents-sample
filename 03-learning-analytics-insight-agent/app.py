import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Learning Analytics Insights Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Learning Analytics Insights Agent")

st.write(
    "AI-assisted learning operations analytics prototype using synthetic enterprise reporting data."
)

# Load synthetic learning data
df = pd.read_csv("../sample-data/learning-metrics.csv")

# Top metrics
col1, col2, col3 = st.columns(3)

with col1:
    avg_completion = round(df["CompletionRate"].mean(), 1)
    st.metric("Average Completion Rate", f"{avg_completion}%")

with col2:
    total_overdue = df["OverdueTraining"].sum()
    st.metric("Total Overdue Trainings", total_overdue)

with col3:
    total_learners = df["LearnerCount"].sum()
    st.metric("Total Learners", total_learners)

st.markdown("---")

# Completion rate visualization
st.subheader("Completion Rates by Department")

fig = px.bar(
    df,
    x="Department",
    y="CompletionRate",
    color="RiskLevel",
    title="Completion Rate Overview"
)

st.plotly_chart(fig, use_container_width=True)

# Overdue training visualization
st.subheader("Overdue Training Volume")

fig2 = px.bar(
    df,
    x="Department",
    y="OverdueTraining",
    color="RiskLevel",
    title="Overdue Training Risk Areas"
)

st.plotly_chart(fig2, use_container_width=True)

st.success(
    "Synthetic learning analytics dashboard loaded successfully."
)