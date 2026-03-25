import streamlit as st
import detector

st.set_page_config(page_title="Scam Detector", page_icon="🛡️")

st.title("🛡️ Multilingual Scam Detector")
st.markdown("### 🔍 Analyze suspicious messages instantly")
st.caption("Detect phishing messages via Text, Image, or Audio in English, Hindi and Marathi")

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Text", "🖼️ Image", "🎤 Audio"])

# ---------------- TEXT INPUT ----------------
with tab1:
    user_input = st.text_area("Enter message")

    if st.button("Analyze Text"):
        if user_input.strip() == "":
            st.warning("Please enter a message")
        else:
            result = detector.detect_scam(user_input)

            if result["threat"] == "phishing":
                st.error("🚨 PHISHING DETECTED")
            elif result["threat"] == "suspicious":
                st.warning("⚠️ Suspicious Message")
            else:
                st.success("✅ Safe Message")

            st.metric(label="Risk Score", value=result["score"])
            st.markdown("---")

            st.subheader("Explanation")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.explanations.get(r, "Unknown"))
            else:
                st.info("No strong threat indicators detected.")

            st.markdown("---")
            st.subheader("Advice")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.advice_map.get(r, "Be cautious"))

# ---------------- IMAGE INPUT (EasyOCR) ----------------
with tab2:
    uploaded_file = st.file_uploader("Upload image (SMS screenshot)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        from PIL import Image
        import numpy as np
        import easyocr

        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        try:
            reader = easyocr.Reader(['en'])  # add 'hi' if needed
            img_array = np.array(image)

            results = reader.readtext(img_array, detail=0)
            text = " ".join(results)

            st.subheader("Extracted Text")
            st.write(text)

            result = detector.detect_scam(text)

            if result["threat"] == "phishing":
                st.error("🚨 PHISHING DETECTED")
            elif result["threat"] == "suspicious":
                st.warning("⚠️ Suspicious Message")
            else:
                st.success("✅ Safe Message")

            st.metric(label="Risk Score", value=result["score"])
            st.markdown("---")

            st.subheader("Explanation")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.explanations.get(r, "Unknown"))
            else:
                st.info("No strong threat indicators detected.")
 
            st.markdown("---")
            st.subheader("Advice")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.advice_map.get(r, "Be cautious"))

        except Exception as e:
            st.error(f"OCR failed: {e}")

# ---------------- AUDIO INPUT ----------------
with tab3:
    audio_file = st.file_uploader("Upload audio (WAV recommended)", type=["wav", "mp3"])

    if audio_file:
        import speech_recognition as sr

        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)

            text = recognizer.recognize_google(audio_data)

            st.subheader("Recognized Speech")
            st.write(text)

            result = detector.detect_scam(text)

            if result["threat"] == "phishing":
                st.error("🚨 PHISHING DETECTED")
            elif result["threat"] == "suspicious":
                st.warning("⚠️ Suspicious Message")
            else:
                st.success("✅ Safe Message")

            st.metric(label="Risk Score", value=result["score"])
            st.markdown("---")

            st.subheader("Explanation")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.explanations.get(r, "Unknown"))
            else:
                st.info("No strong threat indicators detected.")

            st.markdown("---")
            st.subheader("Advice")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.advice_map.get(r, "Be cautious"))

        except Exception:
            st.error("Could not process audio. Please upload a clear WAV/MP3 file.")

st.caption("ThIS TOOL PROVIDES ADVISORY DETECTION. ALWAYS VERIFY WITH OFFICIAL SOURCES.")
