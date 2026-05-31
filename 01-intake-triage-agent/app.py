import os
import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(
    page_title="Learning Intake Triage Agent",
    page_icon="📋",
    layout="wide"
)

# -----------------------------
# OpenAI Setup
# -----------------------------

client = None

if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("Northstar Learning CoE")
st.sidebar.write(
    "Simulated enterprise learning operations prototype using fictional business scenarios."
)

st.sidebar.markdown("---")

st.sidebar.subheader("Prototype Purpose")
st.sidebar.write(
    "This tool helps triage learning requests by estimating priority, risk, delivery approach, and next steps."
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Portfolio project using synthetic scenarios only. No proprietary data is included."
)

# -----------------------------
# Main Header
# -----------------------------

st.title("📋 Learning Intake Triage Agent")

st.write(
    "A simulated decision-support tool for prioritizing enterprise learning requests."
)

st.info(
    "Use this prototype to evaluate a fictional training request based on urgency, compliance risk, business impact, audience size, and stakeholder complexity."
)

# -----------------------------
# Intake Form
# -----------------------------

st.header("Training Request Details")

request = st.text_area(
    "Describe the training request",
    height=140,
    placeholder="Example: The Customer Support Operations team needs mandatory training on upcoming regulatory changes impacting member communications..."
)

col1, col2 = st.columns(2)

with col1:
    audience_size = st.selectbox(
        "Audience size",
        [
            "Small: under 100",
            "Medium: 100-1,000",
            "Large: 1,000+"
        ]
    )

    urgency = st.selectbox(
        "Urgency",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    business_impact = st.selectbox(
        "Business impact",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

with col2:
    compliance_risk = st.selectbox(
        "Compliance or regulatory risk?",
        [
            "No",
            "Maybe",
            "Yes"
        ]
    )

    stakeholder_complexity = st.selectbox(
        "Stakeholder complexity",
        [
            "Single team",
            "Cross-functional",
            "Enterprise-wide"
        ]
    )

    requested_delivery = st.selectbox(
        "Requested delivery type",
        [
            "Unsure",
            "eLearning",
            "Instructor-led",
            "Microlearning",
            "Blended"
        ]
    )

# -----------------------------
# Scoring Logic
# -----------------------------

def calculate_priority_score(
    audience_size,
    urgency,
    compliance_risk,
    business_impact,
    stakeholder_complexity
):
    score = 0

    urgency_scores = {"Low": 1, "Medium": 2, "High": 3}
    compliance_scores = {"No": 0, "Maybe": 2, "Yes": 3}
    business_impact_scores = {"Low": 1, "Medium": 2, "High": 3}
    audience_scores = {
        "Small: under 100": 1,
        "Medium: 100-1,000": 2,
        "Large: 1,000+": 3
    }
    stakeholder_scores = {
        "Single team": 1,
        "Cross-functional": 2,
        "Enterprise-wide": 3
    }

    score += urgency_scores[urgency]
    score += compliance_scores[compliance_risk]
    score += business_impact_scores[business_impact]
    score += audience_scores[audience_size]
    score += stakeholder_scores[stakeholder_complexity]

    return score


def determine_priority(score):
    if score >= 12:
        return "High"
    elif score >= 8:
        return "Medium"
    else:
        return "Low"


def determine_risk_level(compliance_risk, stakeholder_complexity, urgency):
    if compliance_risk == "Yes" or stakeholder_complexity == "Enterprise-wide":
        return "High"
    elif compliance_risk == "Maybe" or urgency == "High":
        return "Medium"
    else:
        return "Low"


def recommend_timeline(priority, compliance_risk):
    if priority == "High" and compliance_risk == "Yes":
        return "4–6 weeks with accelerated stakeholder review"
    elif priority == "High":
        return "4–6 weeks"
    elif priority == "Medium":
        return "6–8 weeks"
    else:
        return "8–12 weeks or backlog review"


def recommend_delivery(requested_delivery, audience_size, compliance_risk):
    if requested_delivery != "Unsure":
        return requested_delivery

    if compliance_risk == "Yes":
        return "Required eLearning with knowledge check and reporting visibility"
    elif audience_size == "Large: 1,000+":
        return "Scalable eLearning or microlearning campaign"
    else:
        return "Microlearning or targeted performance support"


def determine_escalation(priority, stakeholder_complexity, compliance_risk):
    if priority == "High" or stakeholder_complexity == "Enterprise-wide" or compliance_risk == "Yes":
        return "Yes"
    else:
        return "No"


# -----------------------------
# AI Summary
# -----------------------------

def generate_ai_summary(
    request,
    priority,
    risk_level,
    timeline,
    delivery_recommendation
):

    prompt = f"""
You are an enterprise learning strategist.

Create a concise executive summary for this fictional training request.

Training Request:
{request}

Priority:
{priority}

Risk Level:
{risk_level}

Recommended Timeline:
{timeline}

Recommended Delivery:
{delivery_recommendation}

Include:
1. Executive Summary
2. Key Risks
3. Suggested Next Actions

Keep the tone concise and executive-level.
"""

    response = client.responses.create(
        model="gpt-5.2",
        input=prompt
    )

    return response.output_text


# -----------------------------
# Results
# -----------------------------

if st.button("Analyze Request", type="primary"):

    if not request.strip():
        st.warning("Please enter a training request before analyzing.")
    else:

        score = calculate_priority_score(
            audience_size,
            urgency,
            compliance_risk,
            business_impact,
            stakeholder_complexity
        )

        priority = determine_priority(score)

        risk_level = determine_risk_level(
            compliance_risk,
            stakeholder_complexity,
            urgency
        )

        timeline = recommend_timeline(priority, compliance_risk)

        delivery_recommendation = recommend_delivery(
            requested_delivery,
            audience_size,
            compliance_risk
        )

        escalation_required = determine_escalation(
            priority,
            stakeholder_complexity,
            compliance_risk
        )

        st.markdown("---")

        st.header("Triage Recommendation")

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric("Priority", priority)

        with metric_col2:
            st.metric("Priority Score", f"{score}/15")

        with metric_col3:
            st.metric("Risk Level", risk_level)

        st.subheader("Recommended Approach")

        st.write(f"**Suggested Timeline:** {timeline}")
        st.write(f"**Recommended Delivery:** {delivery_recommendation}")
        st.write(f"**Escalation Required:** {escalation_required}")

        st.subheader("AI-Generated Executive Brief")

        if not os.getenv("OPENAI_API_KEY"):
            st.error("OpenAI API key not found.")
        else:
            with st.spinner("Generating executive brief..."):

                ai_summary = generate_ai_summary(
                    request,
                    priority,
                    risk_level,
                    timeline,
                    delivery_recommendation
                )

                st.success("AI executive brief generated successfully.")

                st.markdown("### Executive Interpretation")

                st.write(ai_summary)

                st.markdown("---")

                st.caption(
                    "Note: This AI-generated brief is based on synthetic portfolio data and should be reviewed by a human before use."
                )
# ----------------------------------
# Save Intake Request
# ----------------------------------

st.divider()

if st.button("Submit Intake Request"):

    export_record = {
        "Request": request,
        "Audience Size": audience_size,
        "Urgency": urgency,
        "Business Impact": business_impact,
        "Compliance Risk": compliance_risk,
        "Stakeholder Complexity": stakeholder_complexity,
    }

    df_new = pd.DataFrame([export_record])

    file_path = "intake_request_log.csv"

    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path)
        df_updated = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_updated = df_new

    df_updated.to_csv(file_path, index=False)

    st.success("Intake request saved successfully.")

    if os.path.exists("intake_request_log.csv"):
    st.subheader("Saved Intake Requests")
    saved_requests = pd.read_csv("intake_request_log.csv")
    st.dataframe(saved_requests, use_container_width=True)
    