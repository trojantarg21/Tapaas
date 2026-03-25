import streamlit as st
import detector

st.title("🛡️ Scam Detector")
st.caption("Detect phishing messages in English, Hindi, and Marathi")
st.divider()

user_input = st.text_area("Enter message")

if st.button("Analyze"):
    try:
        result = detector.detect_scam(user_input)

        st.write("Threat:", result["threat"])
        st.write("Score:", result["score"])
        st.markdown("---")

        st.subheader("Explanation")
        for r in result["reasons"]:
            st.write("-", detector.explanations.get(r, "Unknown"))

        st.subheader("Advice")
        for r in result["reasons"]:
            st.write("-", detector.advice_map.get(r, "Be cautious"))

    except Exception as e:
        st.error(f"Error: {e}")
