# Security

## API keys (action required)

Earlier versions of this project contained API keys in source code. Those keys are **compromised** if the repository was ever public or shared.

**Rotate immediately:**

1. [Groq Console](https://console.groq.com/) — revoke the old key, create a new one.
2. [OpenRouter](https://openrouter.ai/settings/keys) — revoke the old key, create a new one.

Store new keys only in a local `.env` file (never commit `.env`).

```bash
cp .env.example .env
# Edit .env with your new keys
```

## Running locally

- `.env` is listed in `.gitignore`.
- `app.py` reads `GROQ_API_KEY` and `OPENROUTER_API_KEY` from the environment.
- Optional: `pip install python-dotenv` loads `.env` automatically when present.

## Model artifact

`fraud_model.pkl` is a serialized scikit-learn estimator. Only load pickles you trained yourself or trust from this project.
