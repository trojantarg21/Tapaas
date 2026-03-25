import streamlit as st
from detector import detect_scam

st.title("🛡️ Scam Detector")

user_input = st.text_area("Enter message")

if st.button("Analyze"):
    result = detect_scam(user_input)
    st.write(result)
