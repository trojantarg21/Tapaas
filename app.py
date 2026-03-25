import streamlit as st
from detector import detect_scam
from detector import explanations, advice_map

st.set_page_config(page_title="Scam Detector", page_icon="🛡️")

st.title("Multilingual Scam Detector")
st.write("Analyze suspicious messages using AI + rules")

# Input box
user_input = st.text_area("Enter message to analyze:")

# Button
if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please enter a message")
    else:
        result = detect_scam(user_input)

        # Threat display
        if result["threat"] == "phishing":
            st.error("PHISHING DETECTED")
        elif result["threat"] == "suspicious":
            st.warning("Suspicious Message")
        else:
            st.success("Safe Message")

        st.write("**Score:**", result["score"])

        # Explanation
        st.subheader("Explanation")
        if result["reasons"]:
            for r in result["reasons"]:
                st.write("-", explanations[r])
        else:
            st.write("No major threats detected.")

        # Advice
        st.subheader("Advice")
        if result["reasons"]:
            for r in result["reasons"]:
                st.write("-", advice_map[r])
