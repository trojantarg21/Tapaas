import streamlit as st

st.title("🛡️ Scam Detector")

user_input = st.text_area("Enter message")

if st.button("Analyze"):
    try:
        from detector import detect_scam
        result = detect_scam(user_input)
        st.write(result)
    except Exception as e:
        st.error(f"Error: {e}")
