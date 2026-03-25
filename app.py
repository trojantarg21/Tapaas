import streamlit as st
import detector
from PIL import Image
import pytesseract
import speech_recognition as sr

st.title("🛡️ Scam Detector")
st.caption("Detect phishing messages in English, Hindi, and Marathi")
st.divider()

user_input = st.text_area("Enter message")
uploaded_file = st.file_uploader("Upload an image (SMS screenshot)", type=["png", "jpg", "jpeg"])
audio_file = st.file_uploader("Upload audio message", type=["wav", "mp3"])

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

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    extracted_text = pytesseract.image_to_string(image)

    st.subheader("Extracted Text")
    st.write(extracted_text)

    result = detector.detect_scam(extracted_text)

if audio_file is not None:
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)

        st.subheader("Recognized Speech")
        st.write(text)

        result = detector.detect_scam(text)

    except:
        st.error("Could not understand audio")
