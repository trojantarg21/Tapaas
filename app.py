import streamlit as st
import detector
import os
from datetime import datetime
from langdetect import detect, DetectorFactory
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Devanagari", "NotoSansDevanagari-VariableFont_wdth,wght.ttf"))

DetectorFactory.seed = 0

#LANGUAGE DETECTION
def detect_language_safe(text):
    try:
        if any('\u0900' <= c <= '\u097F' for c in text):
            return "Hindi/Marathi"

        if len(text.split()) < 4:
            return "Not enough text"

        lang = detect(text)
        return {"en": "English", "hi": "Hindi", "mr": "Marathi"}.get(lang, "Unknown")

    except:
        return "Unknown"

#LANGUAGE MAP
def get_explanations_by_language(language):
    if language == "Hindi":
        return detector.explanations_hi
    elif language == "Marathi":
        return detector.explanations_mr
    else:
        return detector.explanations

def get_advice_by_language(language):
    if language == "Hindi":
        return detector.advice_map_hi
    elif language == "Marathi":
        return detector.advice_map_mr
    else:
        return detector.advice_map

#RESULT DISPLAY
def show_results(result, original_text, preferred_lang):

    detected_lang = detect_language_safe(original_text)

    st.info(f"🌍 Detected Language: {detected_lang}")
    st.info(f"🎯 Output Language: {preferred_lang}")

    explanations_map = get_explanations_by_language(preferred_lang)
    advice_map = get_advice_by_language(preferred_lang)

    # Threat display
    if result["threat"] == "phishing":
        st.error("🚨 PHISHING DETECTED")
    elif result["threat"] == "suspicious":
        st.warning("⚠️ Suspicious Message")
    else:
        st.success("✅ Safe Message")

    st.metric(label="Risk Score", value=result["score"])
    st.markdown("---")

    # Explanation
    st.subheader("Explanation")
    if result["reasons"]:
        for r in result["reasons"]:
            st.write("- " + explanations_map.get(r, "No suspicious pattern detected"))
    else:
        st.info("No strong threat indicators detected.")

    st.markdown("---")

    # Advice
    st.subheader("Advice")
    if result["reasons"]:
        for r in result["reasons"]:
            st.write("- " + advice_map.get(r, "No action needed"))

# PDF GENERATION
def generate_pdf(logs):

    file_path = "logs.pdf"

    pdfmetrics.registerFont(TTFont("Devanagari", "NotoSansDevanagari-VariableFont_wdth,wght.ttf"))

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="TitleStyle",
        fontName="Devanagari",
        fontSize=16,
        leading=20,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        name="SubTitle",
        fontName="Devanagari",
        fontSize=10,
        alignment=1
    )

    normal_style = ParagraphStyle(
        name="NormalStyle",
        fontName="Devanagari",
        fontSize=9
    )

    content = []

    #HEADER
    content.append(Paragraph("TAPAAS", title_style))
    content.append(Paragraph("Multilingual Phishing Detection Log Report", subtitle_style))
    content.append(Spacer(1, 12))

    # TABLE DATA
    table_data = [["Timestamp", "Threat", "Score", "Message"]]

    for log in logs:
        try:
            # Example log format:
            # [2026-04-12 20:10:00] PHISHING | Score: 5 | Message: text

            parts = log.split("|")

            timestamp = parts[0].strip().replace("[", "").replace("]", "")
            threat = parts[0].split("]")[1].strip()
            score = parts[1].split(":")[1].strip()
            message = parts[2].replace("Message:", "").strip()

            table_data.append([
                Paragraph(timestamp, normal_style),
                Paragraph(threat, normal_style),
                Paragraph(score, normal_style),
                Paragraph(message, normal_style)
            ])

        except:
            table_data.append(["-", "-", "-", Paragraph(log.strip(), normal_style)])

    #TABLE
    table = Table(table_data, colWidths=[90, 70, 50, 250])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

        ("FONTNAME", (0, 0), (-1, -1), "Devanagari"),

        ("ALIGN", (1, 1), (2, -1), "CENTER"),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ]))

    content.append(table)

    doc.build(content)

    return file_path

#APP UI

st.set_page_config(page_title="Tapaas", page_icon="🛡️")

st.title("🛡️ Tapaas")
st.markdown("### Multilingual Phishing Detection System")
st.caption("Analyze suspicious messages via Text or Image")

st.divider()

#User language preference
preferred_lang = st.selectbox(
    "🌍 Choose your preferred output language",
    ["English", "Hindi", "Marathi"]
)

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Text", "🖼️ Image", "📜 Logs"])

#TEXT
with tab1:
    user_input = st.text_area("Enter message")

    if st.button("Analyze Text"):
        if user_input.strip() == "":
            st.warning("Please enter a message")
        else:
            result = detector.detect_scam(user_input)
            show_results(result, user_input, preferred_lang)

#IMAGE
with tab2:
    uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        from PIL import Image
        import numpy as np
        import easyocr

        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        reader = easyocr.Reader(['en'])
        img_array = np.array(image)

        results = reader.readtext(img_array, detail=0)
        text = " ".join(results)

        st.subheader("Extracted Text")
        st.write(text)

        result = detector.detect_scam(text)
        show_results(result, text, preferred_lang)

# LOGS
with tab3:

    # Clear logs FIRST
    if st.button("🗑️ Clear Logs"):
        with open("logs.txt", "w", encoding="utf-8") as f:
            f.truncate(0)
        st.success("Logs cleared!")
        st.rerun()

    search_query = st.text_input("🔍 Search logs")
    filter_option = st.selectbox("Filter", ["All", "Phishing", "Suspicious", "Safe"])

    if os.path.exists("logs.txt"):
        with open("logs.txt", "r", encoding="utf-8") as f:
            logs = f.readlines()

        filtered_logs = []

        for log in logs:
            if search_query.lower() not in log.lower():
                continue

            if filter_option == "Phishing" and "PHISHING" not in log:
                continue
            elif filter_option == "Suspicious" and "SUSPICIOUS" not in log:
                continue
            elif filter_option == "Safe" and "SAFE" not in log:
                continue

            filtered_logs.append(log)

        if filtered_logs:
            for log in reversed(filtered_logs):
                if "PHISHING" in log:
                    st.error(log)
                elif "SUSPICIOUS" in log:
                    st.warning(log)
                else:
                    st.success(log)

            # PDF Download
            pdf_file = generate_pdf(filtered_logs)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    "📄 Download Logs as PDF",
                    f,
                    file_name="logs.pdf",
                    mime="application/pdf"
                )
        else:
            st.info("No logs found.")
    else:
        st.info("No logs available.")

st.caption("This tool provides advisory detection. Always verify with official sources.")
