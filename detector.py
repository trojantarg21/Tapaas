from rapidfuzz import fuzz
from datetime import datetime
from colorama import Fore, Style, init
init(autoreset=True)

otp_words = ["otp" , "one time password" , "otp dya", "otp pathva" , "otp send" , "otp share", "otp deu", "ओटीपी", "otp dijiye", 
"otp bhejiye", "ओटीपी भेजिये" ]

fear_words = ["account closed", "account terminated", "account band hoil", "account blocked", "account suspended", "अकाउंट ब्लॉक",
"बंद होणार", "account band ho jayega"]

kyc_words = ["kyc", "kyc update", "kyc pending", "verify kyc", "confirm account", "update details", "माहिती अपडेट करा","KYC अपडेट", "update your kyc"]

link_words = ["visit link", "visit the link", "click the link" , "click on the link", "click link", "link vapra", 
"use link", "link visit kara", "link use karo", "link use kara",
"लिंक वापरा" ,"link istemal", "लिंक इस्तेमाल"]

reward_words = ["won a reward", "you won", "congratulations", "abhinandan", "reward milala", "बक्षीस मिळाले आहे", "reward mila", 
"aap jit gaye", "mubarak", "आप जीत गए", "मुबारक", "अभिनंदन" ]

safe_patterns = ["otp share mat karo", "otp share nahi karo","do not share otp","never share otp","otp deu naka", "otp share karu naka", 
"otp mat bhejiye", "otp na bheje", "ओटीपी ना भेजे", "ओ टी पी देउ नका", "otp share mat kare", "ओटीपी शेयर ना करें"]

action_words = [
    "click", "visit", "open", "use", "check", "वापरा" , "इस्तेमाल", "करा", "करें"
    "kar", "kara", "karaycha", "vapra"]

link_indicators = [
    "link", "http", "www", ".com", ".in"]

urgency_words = [
    "urgent", "immediately", "now",
    "jaldi", "turant", "आत्ताच", "जलदी"]

explanations = {
    "otp": "The message is asking for OTP, which is sensitive information.",
    "link": "The message contains a link which could lead to phishing sites.",
    "kyc": "The message is asking for KYC or personal details.",
    "reward": "The message is trying to lure you with a fake reward.",
    "urgency": "The message creates urgency to pressure you." , 
    "action": "The message is requesting for some action"
}

advice_map = {
    "otp": "Never share OTP with anyone.",
    "link": "Do not click unknown links.",
    "kyc": "Do not share personal or banking details.",
    "reward": "Verify rewards from official sources.",
    "urgency": "Take time and verify before acting.",
    "action": "Proceed only after verifying"
}

def fuzzy_match(word, text, threshold=80):
    return fuzz.partial_ratio(word, text) >= threshold

def clean_text(text):
    text = text.lower()
    text = text.replace("0","o")
    text = text.replace(" ","")
    return text


def detect_scam(text):

    reasons = set()

    raw_text = text
    text = clean_text(text)

    safe_detected = False
    for word in safe_patterns: 
     if word in raw_text.lower():
        safe_detected = True
        break

     if safe_detected:
      return {
            "message": raw_text,
            "threat": "safe",
            "score": 0,
            "reasons": []
        }

    action_detected = any(word in raw_text.lower()  for word in action_words)

    link_detected = any(word in raw_text.lower() for word in link_indicators)
    urgency_detected = any(word in raw_text.lower() for word in urgency_words)
    
    otp_detected = any(fuzzy_match(word.replace(" ", ""), text) for word in otp_words)
    kyc_detected = any(fuzzy_match(word.replace(" ", ""), text) for word in kyc_words)
    reward_detected = any(fuzzy_match(word.replace(" ", ""), text) for word in reward_words)

    threat = ""
    score = 0

    #Score updation
    if action_detected:
        score += 1
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
        score +=2
        reasons.add("link")

    #High-risk patterns
    if otp_detected and (action_detected or link_detected):
      threat = "phishing"
      print("OTP + action/link → phishing")

    elif kyc_detected and (link_detected or urgency_detected):
      threat = "phishing"
      print("KYC + link/urgency → phishing")

    elif reward_detected and link_detected: 
      threat = "phishing"
      print("Reward + link → phishing")

    
    #Classification based on scores
    if not threat:  
     if score <= 2:
        threat = "safe"
     elif score <= 4:
        threat = "suspicious"
     else:
        threat = "phishing"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("logs.txt", "a", encoding="utf-8") as f:
      f.write(f"[{timestamp}] {threat.upper()} | Score: {score} | Message: {raw_text}\n")

    return {
        "message": raw_text,
        "threat": threat,
        "score": score,
        "reasons": list(reasons)
    }

while True:
    msg = input("\nEnter message (type 'exit' to quit): ")

    if msg.lower() == "exit":
        print("Exiting tool...")
        break

    detect_scam(msg)