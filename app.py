import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import datetime
import requests as http_requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

st.set_page_config(
    page_title="Aegis — Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

_defaults = {
    "dark_mode":    True,
    "transaction":  None,
    "result":       None,
    "report_text":  None,
    "sample_type":  None,
    "advisor_open": False,
    "advisor_msgs": [],
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

DK          = st.session_state.dark_mode
BG          = "#0a0f1a"   if DK else "#f5f7fb"
SURFACE     = "#111827"   if DK else "#ffffff"
SURFACE2    = "#1a2235"   if DK else "#f0f2f8"
BORDER      = "#1f2d45"   if DK else "#dde3ed"
BORDER2     = "#2a3d5a"   if DK else "#c5cfe0"
TEXT        = "#e8edf8"   if DK else "#0f1928"
TEXT2       = "#6b82a0"   if DK else "#5a6d87"
ACCENT      = "#3b82f6"
ACCENT_BG   = "#1e3a5f"   if DK else "#dbeafe"
ACCENT_TEXT = "#93c5fd"   if DK else "#1d4ed8"
DANGER      = "#ef4444"
DANGER_BG   = "#2d1515"   if DK else "#fef2f2"
DANGER_TXT  = "#fca5a5"   if DK else "#991b1b"
SUCCESS     = "#22c55e"
SUCCESS_BG  = "#0f2d1a"   if DK else "#f0fdf4"
SUCCESS_TXT = "#86efac"   if DK else "#15803d"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"], .stApp {{
    font-family: 'Inter', sans-serif !important;
    background-color: {BG} !important;
    color: {TEXT} !important;
}}
.stApp {{ background-color: {BG} !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 1.5rem 2rem 4rem 2rem !important; max-width: 1100px; }}
section[data-testid="stSidebar"] {{ display: none; }}
.stButton > button {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    border-radius: 8px !important;
    transition: all 0.15s ease !important;
    border: 1px solid {BORDER2} !important;
    background: {SURFACE} !important;
    color: {TEXT} !important;
    padding: 8px 16px !important;
}}
.stButton > button:hover {{
    border-color: {ACCENT} !important;
    color: {ACCENT_TEXT} !important;
    background: {ACCENT_BG} !important;
}}
.stButton > button[kind="primary"] {{
    background: {ACCENT} !important;
    border-color: {ACCENT} !important;
    color: white !important;
}}
.stButton > button[kind="primary"]:hover {{
    background: #2563eb !important;
    border-color: #2563eb !important;
    color: white !important;
}}
.stNumberInput > div > div > input {{
    background: {SURFACE2} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}}
.stTextInput > div > div > input {{
    background: {SURFACE2} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    border-radius: 8px !important;
}}
.stDownloadButton > button {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    border-radius: 8px !important;
    background: {SUCCESS_BG} !important;
    border: 1px solid {SUCCESS} !important;
    color: {SUCCESS_TXT} !important;
}}
hr {{ border-color: {BORDER} !important; margin: 1.2rem 0 !important; }}
.stFormSubmitButton > button {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    border-radius: 8px !important;
    border: 1px solid {BORDER2} !important;
    background: {SURFACE} !important;
    color: {TEXT} !important;
    width: 100% !important;
    height: 38px !important;
    padding: 0 8px !important;
    margin-top: 0px !important;
}}
.stFormSubmitButton > button:hover {{
    border-color: {ACCENT} !important;
    color: {ACCENT_TEXT} !important;
    background: {ACCENT_BG} !important;
}}
label, .stNumberInput label {{
    color: {TEXT2} !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}}
</style>
""", unsafe_allow_html=True)

FRAUD_SAMPLE = {
    "Time": 406.0, "Amount": 2.69,
    "V1": -2.3122265423263,  "V2": 1.9519694437624,   "V3": -1.60985073229769,
    "V4": 3.9979055875468,   "V5": -0.52260268529936,  "V6": -1.4265453192433,
    "V7": -2.53699357509523, "V8": 1.3916154097038,    "V9": -2.7700892408182,
    "V10": -2.7720676909441, "V11": 3.2020369294588,   "V12": -2.8990169504363,
    "V13": -0.5955498695901, "V14": -1.5434888599452,  "V15": 2.302412073175,
    "V16": 1.2577782710617,  "V17": -0.647099765666,   "V18": -1.7461847655827,
    "V19": 0.54000084826551, "V20": 0.3755693571,      "V21": -0.0539124543404,
    "V22": 0.1261234649609,  "V23": -0.1291085618397,  "V24": 0.38940214697384,
    "V25": 0.1865901673284,  "V26": 0.3053462988892,   "V27": -0.1723263428439,
    "V28": 0.1059296937,
}
LEGIT_SAMPLE = {
    "Time": 28800.0, "Amount": 149.62,
    "V1": -1.3598071336738,   "V2": -0.0727811733098497, "V3": 2.53634673796914,
    "V4": 1.37815522427443,   "V5": -0.338320769942518,  "V6": 0.462387777762292,
    "V7": 0.239598554061257,  "V8": 0.0986979012610507,  "V9": 0.363786969611213,
    "V10": 0.0907941719789316,"V11": -0.551599533260813, "V12": -0.617800855762348,
    "V13": -0.991389847235408,"V14": -0.311169353699879, "V15": 1.46817697209427,
    "V16": -0.470400525259478,"V17": 0.207971241929242,  "V18": 0.0257905801985591,
    "V19": 0.403992960255733, "V20": 0.251412098239705,  "V21": -0.018306777944153,
    "V22": 0.277837575558899, "V23": -0.110473910188767, "V24": 0.0669280749146731,
    "V25": 0.128539358273528, "V26": -0.189114843888824, "V27": 0.133558376740387,
    "V28": -0.0210530534538215,
}
FEATURE_COLS = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
DATASET_AMOUNT_MEAN = 88.35

def randomize_pca_features():
    """Generate random PCA feature values from realistic ranges."""
    return {f"V{i}": float(np.random.normal(0, 1)) for i in range(1, 29)}

GROQ_API_KEY       = os.environ.get("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")


@st.cache_resource
def load_model():
    model_path = "fraud_model.pkl"
    if not os.path.exists(model_path):
        return None
    try:
        bundle = joblib.load(model_path)
        if not isinstance(bundle, dict):
            bundle = {"model": bundle, "feature_cols": FEATURE_COLS, "metrics": {}}
        return bundle
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None

def build_behavioural_context(amount, time_val, top_features, fraud_proba):
    if amount < 1.0:
        amount_profile = (f"extremely low (EUR {amount:.2f}) — amounts under EUR 1 are a classic "
            "indicator of card testing, where fraudsters verify a stolen card before making larger purchases")
    elif amount < 10.0:
        amount_profile = (f"very small (EUR {amount:.2f}) — unusually low and consistent with card-testing behaviour")
    elif amount > 1000.0:
        amount_profile = (f"very high (EUR {amount:.2f}) — significantly above the dataset average of EUR {DATASET_AMOUNT_MEAN:.2f}, consistent with high-value fraud")
    else:
        amount_profile = (f"EUR {amount:.2f} — within a normal spending range")

    hours_elapsed = time_val / 3600
    day_num       = int(hours_elapsed // 24) + 1
    hour_of_day   = int(hours_elapsed % 24)
    if 0 <= hour_of_day < 6:
        time_profile = (f"approximately {hour_of_day:02d}:00 on day {day_num} — the early hours, "
            "a period of elevated fraud risk as cardholders are typically asleep")
    else:
        time_profile = (f"approximately {hour_of_day:02d}:00 on day {day_num} — standard activity period")

    strong_anomaly = sum(1 for _, val, _ in top_features if abs(val) > 3.0)
    mild_anomaly   = sum(1 for _, val, _ in top_features if abs(val) > 2.0)
    if strong_anomaly >= 2:
        anomaly_profile = (f"{strong_anomaly} of the top predictive signals show extreme deviation from patterns typical of legitimate transactions")
    elif mild_anomaly >= 2:
        anomaly_profile = (f"{mild_anomaly} signals show notable deviation from normal cardholder behaviour")
    else:
        anomaly_profile = ("transaction signals are broadly consistent with legitimate cardholder activity")

    risk_band = ("CRITICAL" if fraud_proba >= 0.85 else "HIGH" if fraud_proba >= 0.65 else "MEDIUM" if fraud_proba >= 0.40 else "LOW")
    return {"amount_profile": amount_profile, "time_profile": time_profile,
            "anomaly_profile": anomaly_profile, "risk_band": risk_band, "fraud_proba_pct": fraud_proba * 100}

def generate_report(prediction, confidence, fraud_proba, amount, time_val, top_features, ctx):
    if not GROQ_API_KEY:
        return "[ERROR] GROQ_API_KEY not configured."
    try:
        from groq import Groq
    except ImportError:
        return "[ERROR] groq not installed. Run: pip install groq"

    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""You are a senior financial fraud analyst writing an official incident report for a bank compliance team.

PREDICTION: {prediction}
CONFIDENCE: {confidence:.1f}%
FRAUD PROBABILITY: {ctx['fraud_proba_pct']:.1f}%
RISK BAND: {ctx['risk_band']}

TRANSACTION:
- Amount: {ctx['amount_profile']}
- Timing: {ctx['time_profile']}
- Behavioural signals: {ctx['anomaly_profile']}

RULES:
- Never reference column names like V1, V2, V14 etc.
- Describe risk in plain English using fraud domain language only.
- Be specific and actionable. No vague statements.
- Write for a compliance officer, not a data scientist.

Write exactly these five sections:
1. Executive Summary
2. Transaction Analysis
3. Behavioural Risk Indicators
4. Risk Assessment
5. Recommended Actions
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR] Report generation failed: {e}"

def clean_text(text: str) -> str:
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u2012": "-",
        "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2022": "*", "\u2026": "...",
        "\u00e9": "e", "\u00e0": "a", "\u00e8": "e",
        "\u00ea": "e", "\u00fc": "u", "\u00e4": "a",
        "\u00f6": "o", "\u00e7": "c", "\u00a0": " ",
    }
    for char, rep in replacements.items():
        text = text.replace(char, rep)
    return text.encode("latin-1", errors="ignore").decode("latin-1")

def export_pdf(report_text, prediction, confidence, amount, time_val):
    report_text = clean_text(report_text)
    prediction  = clean_text(prediction)
    try:
        from fpdf import FPDF
    except ImportError:
        raise RuntimeError("fpdf2 not installed. Run: pip install fpdf2")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(20, 20, 20)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(10, 10, 10)
    pdf.cell(0, 10, "Fraud Detection Incident Report", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, f"Generated: {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}  |  Aegis Fraud Detection System", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    is_fraud = prediction == "FRAUDULENT"
    pdf.set_fill_color(200, 40, 40) if is_fraud else pdf.set_fill_color(0, 140, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 11, f"  Verdict: {prediction}   |   Confidence: {confidence:.1f}%", new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.ln(3)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Transaction Amount: EUR {amount:.2f}   |   Time Offset: {time_val:.0f} seconds", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 170, pdf.get_y())
    pdf.ln(4)
    pdf.set_text_color(30, 30, 30)
    for line in report_text.split("\n"):
        line = line.strip()
        if not line:
            pdf.ln(2)
            continue
        if len(line) > 2 and line[0].isdigit() and line[1] == ".":
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(0, 70, 150)
            pdf.multi_cell(0, 7, line)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 30, 30)
        elif line.startswith("- ") or line.startswith("* "):
            pdf.set_font("Helvetica", "", 10)
            pdf.set_x(25)
            pdf.multi_cell(0, 6, f"  {line}")
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, line)
    pdf.set_y(-18)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(160, 160, 160)
    pdf.cell(0, 6, "Aegis - Real-Time Credit Card Fraud Detection System | Final Year Project", align="C")
    return bytes(pdf.output())

ADVISOR_SYSTEM = """You are Aegis's expert Fraud Prevention Advisor. You are knowledgeable, friendly, and professional. You specialise exclusively in credit card and payment fraud detection, fraud prevention best practices, risk mitigation, cybersecurity relating to financial transactions, consumer scam awareness, and regulatory guidance around fraud such as GDPR and PSD2. You only answer questions within these domains. If asked about anything unrelated, politely redirect the user. Keep responses concise and practical. Never mention your underlying model name."""

def ask_advisor(messages: list) -> str:
    if not OPENROUTER_API_KEY:
        return "Advisor unavailable: OPENROUTER_API_KEY not configured."
    try:
        payload = {
            "model": "anthropic/claude-opus-4.7",
            "max_tokens": 400,
            "messages": [{"role": "system", "content": ADVISOR_SYSTEM}] + messages,
        }
        response = http_requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"Advisor error: {data['error']['message']}"
        else:
            return f"Unexpected response: {data}"
    except http_requests.exceptions.Timeout:
        return "Request timed out — please try again."
    except Exception as e:
        return f"Advisor unavailable: {e}"

def card(content, padding="20px", extra_style=""):
    return (f'<div style="background:{SURFACE}; border:1px solid {BORDER}; border-radius:12px; padding:{padding}; {extra_style}">{content}</div>')

bundle = load_model()
if bundle is None:
    st.markdown(card(
        f'<p style="color:{DANGER_TXT}; font-weight:600; margin:0 0 6px">Model not found</p>'
        f'<p style="color:{TEXT2}; font-size:13px; margin:0">Place fraud_model.pkl in the same folder as app.py</p>',
        extra_style=f"border-color:{DANGER};"), unsafe_allow_html=True)
    st.stop()

model = bundle["model"]

# ── NAV BAR ──
nav_left, nav_right = st.columns([1, 1])
with nav_left:
    st.markdown(f'<div style="display:flex;align-items:center;gap:10px;padding:8px 0"><span style="font-size:20px">🛡️</span><span style="font-size:17px;font-weight:600;color:{TEXT}">Aegis</span><span style="font-size:12px;color:{TEXT2};margin-left:4px">Fraud Detection</span></div>', unsafe_allow_html=True)
with nav_right:
    toggle_cols = st.columns([2, 1, 1])
    with toggle_cols[1]:
        if st.button("☀ Light" if DK else "🌙 Dark", key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    with toggle_cols[2]:
        if st.button("💬 Advisor ✕" if st.session_state.advisor_open else "💬 Advisor", key="advisor_toggle"):
            st.session_state.advisor_open = not st.session_state.advisor_open
            st.rerun()

st.markdown(f'<hr style="border-color:{BORDER};margin:0 0 1.5rem 0">', unsafe_allow_html=True)

if st.session_state.advisor_open:
    main_col, adv_col = st.columns([6, 4], gap="large")
else:
    main_col = st.columns([1])[0]
    adv_col  = None

# ── DETECTION PANEL ──
with main_col:
    st.markdown(f'<h1 style="font-size:26px;font-weight:600;color:{TEXT};margin:0 0 4px">Transaction Analysis</h1><p style="font-size:13px;color:{TEXT2};margin:0 0 24px">Load a transaction sample, run the analysis, and generate a compliance report.</p>', unsafe_allow_html=True)

    st.markdown(f'<p style="font-size:11px;font-weight:500;letter-spacing:0.06em;text-transform:uppercase;color:{TEXT2};margin-bottom:10px">Select a transaction sample</p>', unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        if st.button("Sample Transaction A", use_container_width=True, key="btn_fraud"):
            st.session_state.transaction = FRAUD_SAMPLE.copy()
            st.session_state.sample_type = "fraud"
            st.session_state.result      = None
            st.session_state.report_text = None
    with sc2:
        if st.button("Sample Transaction B", use_container_width=True, key="btn_legit"):
            st.session_state.transaction = LEGIT_SAMPLE.copy()
            st.session_state.sample_type = "legit"
            st.session_state.result      = None
            st.session_state.report_text = None
    with sc3:
        if st.button("Custom Transaction", use_container_width=True, key="btn_random"):
            custom = randomize_pca_features()
            custom["Time"]   = 0.0
            custom["Amount"] = 100.0
            st.session_state.transaction = custom
            st.session_state.sample_type = "custom"
            st.session_state.result      = None
            st.session_state.report_text = None

    st.divider()

    sample_loaded  = st.session_state.transaction is not None
    default_time   = float(st.session_state.transaction["Time"])   if sample_loaded else 0.0
    default_amount = float(st.session_state.transaction["Amount"]) if sample_loaded else 100.0

    st.markdown(f'<p style="font-size:11px;font-weight:500;letter-spacing:0.06em;text-transform:uppercase;color:{TEXT2};margin-bottom:10px">Transaction details</p>', unsafe_allow_html=True)

    ic1, ic2 = st.columns(2)
    with ic1:
        time_val = st.number_input("Time (seconds elapsed)", value=default_time, step=1.0, format="%.2f", min_value=0.0)
    with ic2:
        amount_val = st.number_input("Amount (EUR)", value=default_amount, step=0.01, format="%.2f", min_value=0.0)

    if st.session_state.transaction:
        st.session_state.transaction["Time"]   = time_val
        st.session_state.transaction["Amount"] = amount_val

    if sample_loaded:
        st.markdown(f'<div style="margin:10px 0;font-size:12px;color:{ACCENT_TEXT};background:{ACCENT_BG};border-radius:6px;padding:7px 12px;border:1px solid {ACCENT}40">&#9679; Transaction loaded — ready to analyse</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="margin:10px 0;font-size:12px;color:{TEXT2};background:{SURFACE2};border-radius:6px;padding:7px 12px;border:1px solid {BORDER}">Select a sample above to load transaction data</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔍  Run Analysis", use_container_width=True, type="primary", key="run_btn"):
        if not sample_loaded:
            st.error("Please load a transaction sample first.")
        else:
            with st.spinner("Analysing transaction..."):
                try:
                    tx       = st.session_state.transaction
                    input_df = pd.DataFrame([tx])[FEATURE_COLS]
                    pred        = model.predict(input_df)[0]
                    proba_arr   = model.predict_proba(input_df)[0]
                    fraud_proba = float(proba_arr[1])
                    confidence  = float(proba_arr[pred]) * 100
                    importances = model.feature_importances_
                    feat_imp    = sorted(zip(FEATURE_COLS, input_df.values[0], importances), key=lambda x: x[2], reverse=True)[:5]
                    st.session_state.result = {
                        "prediction":   "FRAUDULENT" if pred == 1 else "LEGITIMATE",
                        "confidence":   confidence,
                        "fraud_proba":  fraud_proba,
                        "top_features": feat_imp,
                        "amount":       amount_val,
                        "time":         time_val,
                    }
                    st.session_state.report_text = None
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

    if st.session_state.result:
        r        = st.session_state.result
        is_fraud = r["prediction"] == "FRAUDULENT"
        v_colour = DANGER_TXT if is_fraud else SUCCESS_TXT
        v_bg     = DANGER_BG  if is_fraud else SUCCESS_BG
        v_border = DANGER     if is_fraud else SUCCESS
        v_icon   = "&#9888;"  if is_fraud else "&#10003;"
        bar_col  = DANGER     if is_fraud else SUCCESS

        st.markdown(
            f'<div style="background:{v_bg};border:1px solid {v_border}40;border-radius:12px;padding:18px;margin-top:16px">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">'
            f'<span style="font-size:16px;font-weight:600;color:{v_colour}">{v_icon} {r["prediction"]} TRANSACTION</span>'
            f'<span style="font-size:12px;color:{TEXT2};font-family:JetBrains Mono,monospace">Confidence: {r["confidence"]:.1f}%</span>'
            f'</div>'
            f'<div style="height:4px;background:{BORDER};border-radius:2px;margin-bottom:12px">'
            f'<div style="height:4px;width:{r["confidence"]:.1f}%;background:{bar_col};border-radius:2px"></div></div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">'
            f'<div style="background:{SURFACE}40;border-radius:6px;padding:8px 10px"><div style="font-size:10px;color:{TEXT2};text-transform:uppercase;letter-spacing:0.06em">Amount</div><div style="font-size:14px;font-weight:500;color:{TEXT};font-family:JetBrains Mono,monospace">EUR {r["amount"]:.2f}</div></div>'
            f'<div style="background:{SURFACE}40;border-radius:6px;padding:8px 10px"><div style="font-size:10px;color:{TEXT2};text-transform:uppercase;letter-spacing:0.06em">Fraud probability</div><div style="font-size:14px;font-weight:500;color:{v_colour};font-family:JetBrains Mono,monospace">{r["fraud_proba"]*100:.1f}%</div></div>'
            f'<div style="background:{SURFACE}40;border-radius:6px;padding:8px 10px"><div style="font-size:10px;color:{TEXT2};text-transform:uppercase;letter-spacing:0.06em">Time offset</div><div style="font-size:14px;font-weight:500;color:{TEXT};font-family:JetBrains Mono,monospace">{r["time"]:.0f}s</div></div>'
            f'</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📄 Generate Compliance Report", use_container_width=True, key="gen_report"):
            with st.spinner("Generating report — this takes a few seconds..."):
                ctx    = build_behavioural_context(r["amount"], r["time"], r["top_features"], r["fraud_proba"])
                report = generate_report(r["prediction"], r["confidence"], r["fraud_proba"], r["amount"], r["time"], r["top_features"], ctx)
                st.session_state.report_text = report

        if st.session_state.report_text:
            report_text = st.session_state.report_text
            st.divider()
            st.markdown(f'<p style="font-size:11px;font-weight:500;letter-spacing:0.06em;text-transform:uppercase;color:{TEXT2};margin-bottom:12px">Compliance Report</p>', unsafe_allow_html=True)
            if report_text.startswith("[ERROR]"):
                st.error(report_text)
            else:
                st.markdown(f'<div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:20px;font-size:14px;color:{TEXT};line-height:1.75">' + report_text.replace("\n", "<br>") + '</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                try:
                    ctx       = build_behavioural_context(r["amount"], r["time"], r["top_features"], r["fraud_proba"])
                    pdf_bytes = export_pdf(report_text, r["prediction"], r["confidence"], r["amount"], r["time"])
                    ts        = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button(label="⬇  Download as PDF", data=pdf_bytes, file_name=f"aegis_report_{ts}.pdf", mime="application/pdf", use_container_width=True)
                except Exception as e:
                    st.error(f"PDF export failed: {e}")

# ── ADVISOR PANEL ──
if st.session_state.advisor_open and adv_col is not None:
    with adv_col:
        st.markdown(
            f'<div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;overflow:hidden">'
            f'<div style="background:{ACCENT_BG};border-bottom:1px solid {BORDER};padding:14px 18px;display:flex;align-items:center;gap:10px">'
            f'<span style="font-size:18px">🛡️</span>'
            f'<div><div style="font-size:14px;font-weight:600;color:{ACCENT_TEXT}">Fraud Prevention Advisor</div>'
            f'<div style="font-size:11px;color:{TEXT2}">Ask anything about fraud, scams, or security</div></div>'
            f'</div></div>', unsafe_allow_html=True)

        msgs_html = ""
        for msg in st.session_state.advisor_msgs:
            is_user     = msg["role"] == "user"
            bubble_bg   = ACCENT_BG   if is_user else SURFACE2
            bubble_text = ACCENT_TEXT if is_user else TEXT
            align       = "flex-end"  if is_user else "flex-start"
            msgs_html  += (
                f'<div style="display:flex;justify-content:{align};margin-bottom:10px">'
                f'<div style="max-width:85%;background:{bubble_bg};color:{bubble_text};border-radius:10px;padding:10px 14px;font-size:13px;line-height:1.6;border:1px solid {BORDER}">'
                + msg["content"].replace("\n", "<br>") + '</div></div>')

        if not msgs_html:
            msgs_html = f'<div style="text-align:center;color:{TEXT2};font-size:13px;padding:40px 20px">&#128075; Ask me anything about fraud prevention,<br>card security, or scam awareness.</div>'

        st.markdown(f'<div style="background:{SURFACE2};border:1px solid {BORDER};border-radius:8px;padding:14px;height:360px;overflow-y:auto;margin-bottom:10px">' + msgs_html + '</div>', unsafe_allow_html=True)

        # ── FORM prevents Enter from looping ──
        with st.form(key="advisor_form", clear_on_submit=True):
            inp_col, send_col = st.columns([5, 1])
            with inp_col:
                user_input = st.text_input("Message", placeholder="e.g. What is card skimming?", label_visibility="collapsed")
            with send_col:
                send = st.form_submit_button("Send", use_container_width=True)

        if send and user_input.strip():
            user_msg = user_input.strip()
            st.session_state.advisor_msgs.append({"role": "user", "content": user_msg})
            with st.spinner("Thinking..."):
                api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.advisor_msgs]
                reply = ask_advisor(api_messages)
            st.session_state.advisor_msgs.append({"role": "assistant", "content": reply})
            st.rerun()

        if st.session_state.advisor_msgs:
            if st.button("Clear conversation", key="clear_chat"):
                st.session_state.advisor_msgs = []
                st.rerun()