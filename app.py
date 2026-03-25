import streamlit as st
from detector import detect_scam, explanations, advice_map

st.title("🛡️ Multilingual Scam Detector")

user_input = st.text_area("Enter message")

if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please enter a message")
    else:
        result = detect_scam(user_input)

        # Threat
        if result["threat"] == "phishing":
            st.error("🚨 PHISHING DETECTED")
        elif result["threat"] == "suspicious":
            st.warning("⚠️ Suspicious Message")
        else:
            st.success("✅ Safe Message")

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
