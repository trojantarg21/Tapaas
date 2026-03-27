from rapidfuzz import fuzz
from datetime import datetime
from colorama import Fore, Style, init
import re

init(autoreset=True)

# ---------------- WORD LISTS ----------------

otp_words = ["otp","one time password","otp dya","otp pathva","otp send","otp share","otp deu","ओटीपी",
             "otp dijiye","otp bhejiye","ओटीपी भेजिये"]

fear_words = ["account closed","account terminated","account band hoil","account blocked",
              "account suspended","अकाउंट ब्लॉक","बंद होणार","account band ho jayega"]

kyc_words = ["kyc","kyc update","kyc pending","verify kyc","confirm account","update details",
             "माहिती अपडेट करा","KYC अपडेट","update your kyc",
             # NEW multilingual additions
             "kyc update kara","kyc update करा","kyc verify kare","kyc verify करें",
             "kyc verify करा","account verify करा"]

reward_words = ["won a reward","you won","congratulations","abhinandan","reward milala",
                "बक्षीस मिळाले आहे","reward mila","aap jit gaye","mubarak","आप जीत गए",
                "मुबारक","अभिनंदन"]

safe_patterns = ["otp share mat karo","otp share nahi karo","do not share otp","never share otp",
                 "otp deu naka","otp share karu naka","otp mat bhejiye","otp na bheje",
                 "ओटीपी ना भेजे","ओ टी पी देउ नका","otp share mat kare","ओटीपी शेयर ना करें",
                 # NEW awareness additions
                 "do not click unknown links","never click unknown links",
                 "bank will never ask otp","never share otp"]

action_words = ["click","visit","open","use","check","वापरा","इस्तेमाल","करा","करें",
                "kar","kara","karaycha","vapra"]

urgency_words = ["urgent","immediately","now","jaldi","turant","आत्ताच","जलदी"]

explanations = {
    "otp": "The message is asking for OTP, which is sensitive information.",
    "link": "The message contains a link which could lead to phishing sites.",
    "kyc": "The message is asking for KYC or personal details.",
    "reward": "The message is trying to lure you with a fake reward.",
    "fear": "The message uses fear tactics to pressure the user.",
    "urgency": "The message creates urgency to pressure you.",
    "action": "The message is requesting for some action",
    "safe": "No suspicious patterns detected."
}

advice_map = {
    "otp": "Never share OTP with anyone.",
    "link": "Do not click unknown links.",
    "kyc": "Do not share personal or banking details.",
    "reward": "Verify rewards from official sources.",
    "fear": "Do not panic. Verify the message from official sources.",
    "urgency": "Take time and verify before acting.",
    "action": "Proceed only after verifying",
    "safe": "No action needed."
}

explanations_hi = {
    "otp": "यह संदेश OTP मांग रहा है, जो संवेदनशील जानकारी है।",
    "link": "इस संदेश में एक लिंक है जो फ़िशिंग साइट पर ले जा सकता है।",
    "kyc": "यह संदेश KYC या व्यक्तिगत जानकारी मांग रहा है।",
    "reward": "यह संदेश नकली इनाम का लालच दे रहा है।",
    "fear": "यह संदेश डर पैदा करके दबाव बना रहा है।",
    "urgency": "यह संदेश तुरंत कार्रवाई के लिए दबाव बना रहा है।",
    "action": "यह संदेश आपसे कोई कार्रवाई करवाना चाहता है।",
    "safe": "कोई संदिग्ध पैटर्न नहीं मिला।"
}

advice_map_hi = {
    "otp": "किसी के साथ OTP साझा न करें।",
    "link": "अज्ञात लिंक पर क्लिक न करें।",
    "kyc": "अपनी व्यक्तिगत या बैंक जानकारी साझा न करें।",
    "reward": "इनाम को आधिकारिक स्रोत से सत्यापित करें।",
    "fear": "घबराएं नहीं। पहले सत्यापित करें।",
    "urgency": "जल्दीबाज़ी में निर्णय न लें।",
    "action": "कोई भी कार्य करने से पहले जांच करें।",
    "safe": "कोई कार्रवाई आवश्यक नहीं है।"
}

explanations_mr = {
    "otp": "हा संदेश OTP मागत आहे, जी संवेदनशील माहिती आहे.",
    "link": "या संदेशात लिंक आहे जी फिशिंग साइटकडे नेऊ शकते.",
    "kyc": "हा संदेश KYC किंवा वैयक्तिक माहिती मागत आहे.",
    "reward": "हा संदेश खोट्या बक्षिसाचे आमिष दाखवत आहे.",
    "fear": "हा संदेश भीती निर्माण करून दबाव टाकतो.",
    "urgency": "हा संदेश तातडीची भावना निर्माण करतो.",
    "action": "हा संदेश तुमच्याकडून काही कृती करवून घेण्याचा प्रयत्न करतो.",
    "safe": "कोणताही संशयास्पद नमुना आढळला नाही."
}

advice_map_mr = {
    "otp": "कोणालाही OTP शेअर करू नका.",
    "link": "अज्ञात लिंकवर क्लिक करू नका.",
    "kyc": "तुमची वैयक्तिक किंवा बँक माहिती शेअर करू नका.",
    "reward": "बक्षीस अधिकृत स्रोताकडून तपासा.",
    "fear": "घाबरू नका. आधी सत्यापन करा.",
    "urgency": "घाईत निर्णय घेऊ नका.",
    "action": "कोणतीही कृती करण्यापूर्वी तपासा.",
    "safe": "कोणतीही कृती आवश्यक नाही."
}

# ---------------- UTIL FUNCTIONS ----------------

def fuzzy_match(word, text, threshold=80):
    return fuzz.partial_ratio(word, text) >= threshold

# Strong normalization
def clean_text(text):
    text = text.lower()

    replacements = {"0": "o", "1": "i", "3": "e", "@": "a"}
    for k, v in replacements.items():
        text = text.replace(k, v)

    text = re.sub(r"[^\w\s]", "", text)
    text = " ".join(text.split())

    return text

#fixed spacing handling
def normalize_spacing(text):
    words = text.split()
    new_words = []
    buffer = ""

    for w in words:
        if len(w) == 1:
            buffer += w
        else:
            if buffer:
                new_words.append(buffer)
                buffer = ""
            new_words.append(w)

    if buffer:
        new_words.append(buffer)

    return " ".join(new_words)

def has_real_link(text):
    text = text.lower()
    return (
        "http://" in text or
        "https://" in text or
        "www." in text or
        ".com" in text or
        ".in" in text
    )

def log_result(threat, score, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {threat.upper()} | Score: {score} | Message: {message}\n")

def no_suspicious_text(text):
    text_lower = text.lower()
    words = text_lower.split()

    suspicious_words = action_words + urgency_words + ["otp","link","kyc","account","verify"]

    if len(words) <= 2 and text.isalpha():
        if not any(word in text_lower for word in suspicious_words):
            return True

    return False

def is_single_word(text):
    return len(text.strip().split()) == 1

# ---------------- MAIN FUNCTION ----------------

def detect_scam(text):

    reasons = set()
    threat = ""
    score = 0

    raw_text = text

    # Safe override
    if no_suspicious_text(text) or is_single_word(text):
        log_result("safe", 0, raw_text)
        return {
            "message": raw_text,
            "threat": "safe",
            "score": 0,
            "reasons": ["safe"]
        }

    # Normalize
    text = clean_text(text)
    text = normalize_spacing(text)

    # Awareness messages
    if any(word in raw_text.lower() for word in safe_patterns):
        log_result("safe", 0, raw_text)
        return {
            "message": raw_text,
            "threat": "safe",
            "score": 0,
            "reasons": ["safe"]
        }

    # Detection signals
    action_detected = any(word in text for word in action_words)
    fear_detected = any(word in text for word in fear_words)
    urgency_detected = any(word in text for word in urgency_words)

    link_detected = has_real_link(text)
    link_word_detected = "link" in text

    otp_detected = any(fuzzy_match(word.replace(" ", ""), text) for word in otp_words)
    kyc_detected = any(fuzzy_match(word.replace(" ", ""), text) for word in kyc_words)
    reward_detected = any(fuzzy_match(word.replace(" ", ""), text) for word in reward_words)

    # Scoring
    if action_detected:
        score += 2   # boosted
        reasons.add("action")

    if fear_detected:
        score += 2
        reasons.add("fear")

    if urgency_detected:
        score += 2
        reasons.add("urgency")

    if otp_detected:
        score += 3
        reasons.add("otp")

    if kyc_detected:
        score += 2
        reasons.add("kyc")

    if reward_detected:
        score += 1
        reasons.add("reward")

    if link_detected:
        score += 2
        reasons.add("link")
    elif link_word_detected and action_detected:
        score += 1
        reasons.add("action")

    # High-risk patterns
    if otp_detected and (action_detected or link_detected):
        threat = "phishing"

    elif kyc_detected and link_detected:
        threat = "phishing"

    elif reward_detected and link_detected:
        threat = "phishing"

    # Low-context override
    if not threat and score >= 2 and len(raw_text.split()) <= 3:
        threat = "suspicious"

    # Classification
    if not threat:
        if score <= 2:
            threat = "safe"
        elif score <= 4:
            threat = "suspicious"
        else:
            threat = "phishing"

    log_result(threat, score, raw_text)

    return {
        "message": raw_text,
        "threat": threat,
        "score": score,
        "reasons": list(reasons)
    }
