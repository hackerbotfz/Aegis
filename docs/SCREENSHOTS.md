# Screenshots for README

Add three PNGs here, then link them from `README.md`:

| File | What to capture |
|------|-----------------|
| `analysis.png` | Transaction Analysis with a verdict after **Run Analysis** |
| `report.png` | Generated compliance report + **Download as PDF** |
| `advisor.png` | Fraud Prevention Advisor panel open with a sample Q&A |

## How to capture

1. Copy `.env.example` to `.env` and add API keys.
2. Extract `fraud_model.pkl` from `fraud_model.zip`.
3. Run `streamlit run app.py`.
4. Use **Win + Shift + S** (Windows) or your OS screenshot tool.
5. Save crops at roughly 1200px wide for a clean README layout.

## README snippet (after files exist)

```markdown
## Screenshots

<p align="center">
  <img src="docs/analysis.png" alt="Transaction analysis" width="48%" />
  <img src="docs/report.png" alt="Compliance report" width="48%" />
</p>
<p align="center">
  <img src="docs/advisor.png" alt="Fraud prevention advisor" width="70%" />
</p>
```
