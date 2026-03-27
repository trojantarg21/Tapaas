import streamlit as st
import detector

st.set_page_config(page_title="Scam Detector", page_icon="🛡️")

st.title("🛡️ Multilingual Scam Detector")
st.markdown("### 🔍 Analyze suspicious messages instantly")
st.caption("Detect phishing messages via Text, Image, or Audio in English, Hindi and Marathi")

st.divider()

# ---------- Helper Functions ----------

def get_color(threat):
    if threat == "safe":
        return "green"
    elif threat == "suspicious":
        return "orange"
    else:
        return "red"

def highlight_text(text, reasons):
    keywords = {
        "otp": ["otp"],
        "link": ["http", "www", "link"],
        "kyc": ["kyc"],
        "urgency": ["urgent", "now", "immediately"],
        "action": ["click", "visit", "open"],
        "fear": ["blocked", "suspended", "closed"]
    }

    text_lower = text.lower()

    for r in reasons:
        for word in keywords.get(r, []):
            if word in text_lower:
                text = text.replace(word, f":red[{word}]")

    return text

def show_results(result, original_text):
    threat = result["threat"]
    score = result["score"]
    reasons = result["reasons"]

    color = get_color(threat)

    # Threat Display
    st.markdown(f"""
    ### 🛡️ Threat Level: <span style='color:{color}'>{threat.upper()}</span>
    """, unsafe_allow_html=True)

    # Score
    st.metric(label="Risk Score", value=score)
    st.progress(min(score / 6, 1.0))

    st.markdown("---")

    # Highlighted Message
    st.subheader("Analyzed Message")
    highlighted = highlight_text(original_text, reasons)
    st.markdown(highlighted)

    st.markdown("---")

    # Explanation
    st.subheader("Explanation")

    if reasons:
        for r in reasons:
            st.write("- " + detector.explanations.get(r, "No suspicious pattern detected"))
    else:
        st.success("No suspicious patterns detected.")

    st.markdown("---")

    # Advice
    st.subheader("Advice")

    if reasons:
        for r in reasons:
            st.write("- " + detector.advice_map.get(r, "No action needed"))
    else:
        st.success("No action needed. This message appears safe.")

# ---------- Tabs ----------

tab1, tab2, tab3, tab4 = st.tabs(["📝 Text", "🖼️ Image", "🎤 Audio", "📜 Logs"])

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

            show_results(result, user_input)

# ---------------- IMAGE INPUT ----------------
with tab2:
    uploaded_file = st.file_uploader("Upload image (SMS screenshot)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        from PIL import Image
        import numpy as np
        import easyocr

        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        try:
            reader = easyocr.Reader(['en'])
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

            show_results(result, text)

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

            show_results(result, text)

        except Exception:
            st.error("Could not process audio. Please upload a clear WAV/MP3 file.")

# ---------------- LOGS VIEWER ----------------
with tab4:
    st.subheader("📜 Detection Logs")

    try:
        with open("logs.txt", "r", encoding="utf-8") as f:
            logs = f.readlines()

        if not logs:
            st.info("No logs available yet.")
        else:
            # Show latest first
            logs = logs[::-1]

            # Optional: limit to last 20 logs
            logs = logs[:20]

            for log in logs:
                if "PHISHING" in log:
                    st.error(log.strip())
                elif "SUSPICIOUS" in log:
                    st.warning(log.strip())
                else:
                    st.success(log.strip())

    except FileNotFoundError:
        st.warning("No logs file found yet. Run some detections first.")

    if st.button("🗑️ Clear Logs"):
      with open("logs.txt", "w", encoding="utf-8") as f:
        f.truncate(0)

      st.success("Logs cleared!")
      st.rerun()

    with open("logs.txt", "r", encoding="utf-8") as f:
       st.download_button("⬇️ Download Logs", f, file_name="logs.txt")



st.caption("THIS TOOL PROVIDES ADVISORY DETECTION. ALWAYS VERIFY WITH OFFICIAL SOURCES.")
