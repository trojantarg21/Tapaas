import streamlit as st
import detector

st.set_page_config(page_title="Scam Detector", page_icon="🛡️")

st.title("🛡️ Multilingual Scam Detector")
st.caption("Detect phishing messages in Text, Image, and Audio in English, Hindi and Marathi")

st.divider()

# Tabs for input modes
tab1, tab2, tab3 = st.tabs(["📝 Text", "🖼️ Image", "🎤 Audio"])

#TEXT INPUT
with tab1:
    user_input = st.text_area("Enter message")

    if st.button("Analyze Text"):
        if user_input.strip() == "":
            st.warning("Please enter a message")
        else:
            result = detector.detect_scam(user_input)

            # Output
            if result["threat"] == "phishing":
                st.error("🚨 PHISHING DETECTED")
            elif result["threat"] == "suspicious":
                st.warning("⚠️ Suspicious Message")
            else:
                st.success("✅ Safe Message")

            st.write("### Score:", result["score"])

            st.markdown("---")

            # Explanation
            st.subheader("Explanation")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.explanations.get(r, "Unknown"))
            else:
                st.info("No strong threat indicators detected.")

            # Advice
            st.subheader("Advice")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.advice_map.get(r, "Be cautious"))

#IMAGE INPUT
with tab2:
    uploaded_file = st.file_uploader("Upload image (SMS screenshot)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        from PIL import Image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        try:
            import pytesseract
            text = pytesseract.image_to_string(image)

            st.subheader("Extracted Text")
            st.write(text)

            result = detector.detect_scam(text)

            # Output
            if result["threat"] == "phishing":
                st.error("🚨 PHISHING DETECTED")
            elif result["threat"] == "suspicious":
                st.warning("⚠️ Suspicious Message")
            else:
                st.success("✅ Safe Message")

            st.write("### Score:", result["score"])

            st.markdown("---")

            st.subheader("Explanation")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.explanations.get(r, "Unknown"))
            else:
                st.info("No strong threat indicators detected.")

            st.subheader("Advice")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.advice_map.get(r, "Be cautious"))

        except:
            st.warning("OCR may not work on cloud. Try text input instead.")

#AUDIO INPUT
with tab3:
    audio_file = st.file_uploader("Upload audio message (WAV recommended)", type=["wav", "mp3"])

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

            # Output
            if result["threat"] == "phishing":
                st.error("🚨 PHISHING DETECTED")
            elif result["threat"] == "suspicious":
                st.warning("⚠️ Suspicious Message")
            else:
                st.success("✅ Safe Message")

            st.write("### Score:", result["score"])

            st.markdown("---")

            st.subheader("Explanation")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.explanations.get(r, "Unknown"))
            else:
                st.info("No strong threat indicators detected.")

            st.subheader("Advice")
            if result["reasons"]:
                for r in result["reasons"]:
                    st.write("- " + detector.advice_map.get(r, "Be cautious"))

        except:
            st.error("Could not process audio. Please upload a clear file.")
