## Overview

**Tapaas** is a multilingual phishing detection system designed to analyze suspicious messages and classify them as **Safe**, **Suspicious**, or **Phishing**.  

The system focuses on **explainability, robustness, and usability**, making it easier for users to understand why a message is flagged.

## Features

- **Multilingual Support**
  - Supports English, Hindi, and Marathi inputs

- **Explainable Detection**
  - Provides reasons for classification (OTP request, link, urgency, etc.)
  - Gives actionable advice to users

- **Robust Against Obfuscation**
  - Handles inputs like:
    - `0tp` → OTP
    - `cl1ck` → click
    - `c l i c k` → click

- **User-Friendly Interface**
  - Built using Streamlit
  - Supports Text and Image (OCR) inputs

- **Logging System**
  - Records all detections in `logs.txt`
  - View logs in UI
  - Filter and search logs

- **PDF Export**
  - Download logs as PDF for audit purposes

## System Architecture

User Input

↓

Preprocessing (Normalization + Cleaning)

↓

Detection Engine (Rule-Based)

↓

Scoring Mechanism

↓

Classification (Safe / Suspicious / Phishing)

↓

Explainable Output + Advice

↓

Logging System

## Detection Approach

Tapaas uses a **rule-based detection engine** that identifies patterns such as:

- OTP requests  
- KYC verification messages  
- Suspicious links  
- Urgency and fear tactics  
- Reward-based scams  

Each detected pattern contributes to a **risk score**, which determines the final classification.

## Adversarial Testing

The system has been tested against:

- Obfuscation attacks (`0tp`, `cl1ck`)
- Spacing attacks (`c l i c k`)
- Mixed-language inputs
- Short-context messages
- Awareness/safe messages

## Installation
git clone <your-repo-link>

cd tapaas

pip install -r requirements.txt

## Running the app
streamlit run app.py 

## Limitations
Rule-based system may miss completely new attack patterns
Language detection may be unreliable for very short inputs
No machine learning model used (can be added in future)

## Future Enhancements
Integration of Machine Learning models
Improved language detection
Voice-based advisory output

## License
This project is for educational purposes
Real-time message monitoring

