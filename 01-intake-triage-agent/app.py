import streamlit as st

st.title("Learning Intake Triage Agent")

st.write(
    "This simulated tool helps triage enterprise learning requests using fictional business scenarios."
)

request = st.text_area(
    "Describe the training request"
)

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

compliance_risk = st.selectbox(
    "Compliance or regulatory risk?",
    [
        "No",
        "Maybe",
        "Yes"
    ]
)

if st.button("Analyze Request"):

    priority = "Medium"

    if urgency == "High" or compliance_risk == "Yes":
        priority = "High"

    elif urgency == "Low" and compliance_risk == "No":
        priority = "Low"

    st.subheader("Triage Summary")

    st.write(f"**Priority:** {priority}")
    st.write(f"**Audience:** {audience_size}")
    st.write(f"**Urgency:** {urgency}")
    st.write(f"**Compliance Risk:** {compliance_risk}")

    st.subheader("Recommended Next Steps")

    st.write("- Clarify business outcome")
    st.write("- Confirm learner audience")
    st.write("- Identify stakeholders")
    st.write("- Determine delivery modality")