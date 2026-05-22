<div align="center">

# Aegis

### Real-time credit card fraud detection

[![Final Year Project](https://img.shields.io/badge/Nottingham%20Trent%20University-Final%20Year%20Project-008080?style=for-the-badge)](https://www.ntu.ac.uk/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

<br/>

[![F1 Score](https://img.shields.io/badge/F1-0.827-22c55e?style=flat-square)]()
[![ROC AUC](https://img.shields.io/badge/ROC%20AUC-0.963-3b82f6?style=flat-square)]()
[![Precision](https://img.shields.io/badge/Precision-0.881-8b5cf6?style=flat-square)]()
[![Recall](https://img.shields.io/badge/Recall-0.779-f59e0b?style=flat-square)]()

<br/>

[![Groq](https://img.shields.io/badge/Groq-LLM%20Reports-000000?style=flat-square)](https://groq.com/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Advisor-6366f1?style=flat-square)](https://openrouter.ai/)
[![imbalanced-learn](https://img.shields.io/badge/imbalanced--learn-SMOTE-e11d48?style=flat-square)]()

<br/>

[![GitHub last commit](https://img.shields.io/github/last-commit/hackerbotfz/FYP?style=flat-square&logo=github)](https://github.com/hackerbotfz/FYP/commits)
[![GitHub repo size](https://img.shields.io/github/repo-size/hackerbotfz/FYP?style=flat-square&logo=github)](https://github.com/hackerbotfz/FYP)
[![GitHub stars](https://img.shields.io/github/stars/hackerbotfz/FYP?style=flat-square&logo=github)](https://github.com/hackerbotfz/FYP/stargazers)

<br/>

**[Faiz Lawan](https://github.com/hackerbotfz)** · N1258521 · BSc (Hons) Computer Science

</div>

---

Aegis scores credit card transactions in real time, surfaces fraud probability and behavioural signals, and produces compliance-ready incident reports with PDF export. A domain-scoped fraud-prevention advisor sits alongside the analyst workflow.

## Overview

Financial fraud detection must balance accuracy with interpretability for compliance and operations teams. Aegis combines a **Random Forest** classifier on severely imbalanced transaction data with **LLM-generated** narrative reports and a conversational advisor—delivered through a **Streamlit** interface with light/dark themes.

| Layer | Role |
|-------|------|
| **ML** | Real-time classification on 30 features (`Time`, `Amount`, PCA components `V1`–`V28`) |
| **Enrichment** | Rule-based behavioural context (card-testing patterns, off-hours activity, signal anomalies) |
| **LLM** | Structured compliance reports (Groq / Llama 3.1) and fraud-prevention Q&A (OpenRouter) |
| **Export** | Timestamped PDF incident reports |

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

## Model performance

| Metric | Score |
|--------|-------|
| F1 | 0.827 |
| Precision | 0.881 |
| Recall | 0.779 |
| ROC AUC | 0.963 |

## Run

```bash
pip install -r requirements.txt
unzip fraud_model.zip    # Windows: Expand-Archive fraud_model.zip
streamlit run app.py
```

`GROQ_API_KEY` and `OPENROUTER_API_KEY` enable report generation and the advisor chat.

## Repository

```
FYP/
├── app.py
├── requirements.txt
├── fraud_model.zip
└── README.md
```

## License

© Faiz Lawan, Nottingham Trent University.
