# Aegis — Real-Time Credit Card Fraud Detection

**Final Year Project · Nottingham Trent University · BSc (Hons) Computer Science**

Aegis scores credit card transactions in real time, surfaces fraud probability and behavioural signals, and produces compliance-ready incident reports with PDF export. A domain-scoped fraud-prevention advisor sits alongside the analyst workflow.

**[Faiz Lawan](https://github.com/hackerbotfz)** · N1258521

---

## Overview

Financial fraud detection must balance accuracy with interpretability for compliance and operations teams. Aegis combines a **Random Forest** classifier on severely imbalanced transaction data with **LLM-generated** narrative reports and a conversational advisor—delivered through a **Streamlit** interface with light/dark themes.

| Layer | Role |
|-------|------|
| **ML** | Real-time classification on 30 features (`Time`, `Amount`, PCA components `V1`–`V28`) |
| **Enrichment** | Rule-based behavioural context (card-testing patterns, off-hours activity, signal anomalies) |
| **LLM** | Structured compliance reports (Groq / Llama 3.1) and fraud-prevention Q&A (OpenRouter) |
| **Export** | Timestamped PDF incident reports |

---

## Architecture

```mermaid
flowchart LR
    subgraph Input
        TX[Transaction vector]
    end

    subgraph ML["Scikit-learn"]
        PKL[(fraud_model.pkl)]
        TX --> PKL
        PKL --> PRED[Prediction + probabilities]
        PKL --> FEAT[Feature importances]
    end

    subgraph Enrichment
        PRED --> CTX[Behavioural context]
        FEAT --> CTX
    end

    subgraph LLM
        CTX --> GROQ[Groq — compliance report]
        CHAT[User messages] --> OR[OpenRouter — advisor]
    end

    subgraph Output
        GROQ --> UI[Streamlit UI]
        OR --> UI
        GROQ --> PDF[PDF export]
    end
```

Trained on the [ULB MLG Credit Card Fraud](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) dataset—284,807 transactions, 0.172% fraud rate—with **SMOTE** resampling and `class_weight='balanced'` on a 200-tree ensemble.

---

## Model performance

Hold-out test set:

| Metric | Score |
|--------|-------|
| F1 | 0.827 |
| Precision | 0.881 |
| Recall | 0.779 |
| ROC AUC | 0.963 |

---

## Tech stack

Python · Streamlit · scikit-learn · imbalanced-learn · pandas · numpy · joblib · Groq · OpenRouter · fpdf2

---

## Run

```bash
pip install -r requirements.txt
unzip fraud_model.zip    # Windows: Expand-Archive fraud_model.zip .
streamlit run app.py
```

`GROQ_API_KEY` and `OPENROUTER_API_KEY` enable report generation and the advisor chat.

---

## Repository

```
FYP/
├── app.py
├── requirements.txt
├── fraud_model.zip
└── README.md
```

---

## License

© Faiz Lawan, Nottingham Trent University.
