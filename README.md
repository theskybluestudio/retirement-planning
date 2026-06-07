# Retirement Planning Suite

A Streamlit-based retirement planning workspace for exploring common retirement questions such as readiness, Roth conversions, Social Security timing, IRMAA exposure, withdrawal strategy, and sequence risk.

## Included tools

- Shared Assumptions
- RMD / Roth Conversion Strategy
- Retirement Readiness
- Social Security Optimizer
- Medicare IRMAA
- Sequence Risk Visualizer
- Safe Withdrawal Guardrails
- Withdrawal Order
- Spending Smile Planner
- Savings Rate / Catch-Up

## Stack

- Python
- Streamlit
- pandas
- numpy
- plotly

## Structure

```text
retirement-planning/
├── application/
│   ├── app.py                 # Main Streamlit entrypoint
│   ├── app_state.py           # Shared session-state defaults and helpers
│   ├── app_i18n.py            # Language strings / i18n support
│   ├── app_ui.py              # Shared UI helpers
│   ├── app_shell.py           # Shared page setup
│   ├── app_pages_*.py         # Calculator page implementations
│   └── pages/                 # Streamlit multipage wrappers
├── requirements.txt
└── requirements.lock.txt
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
cd application
streamlit run app.py --server.port 8501
```

Then open the local Streamlit URL shown in the terminal.

## Notes

- Main entrypoint: `application/app.py`
- Common assumptions are shared across pages through session state
- `runapp.bat` is intentionally excluded from version control as a local helper
- `requirements.lock.txt` is kept alongside `requirements.txt`

## Disclaimer

This project is for educational planning and estimation only. It is not tax, legal, investment, or financial advice.
