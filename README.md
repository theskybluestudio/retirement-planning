# Retirement Planning, Demystified

A Streamlit-based retirement planning workspace for exploring common retirement questions such as retirement readiness, Roth conversions, Social Security timing, Medicare IRMAA exposure, withdrawal strategy, spending patterns, savings rate, and sequence risk.

## Included tools

- Home
- Shared Assumptions
- Retirement Readiness
- Social Security Optimizer
- Savings Rate / Catch-Up
- Spending Smile Planner
- Mega Backdoor Roth
- RMD / Roth Conversion Strategy
- Medicare IRMAA
- Sequence Risk Visualizer
- Safe Withdrawal Guardrails
- Withdrawal Order
- Feedback

## Current features

- Shared assumptions across calculators via Streamlit session state
- English / Chinese language support
- Cookie-based language persistence
- JSON export / import for shared assumptions
- Plain-language explainers embedded in calculator pages
- Dedicated feedback page with GitHub issue and support links

## Stack

- Python
- Streamlit
- pandas
- numpy
- plotly
- st-cookie

## Structure

```text
retirement-planning/
├── application/
│   ├── app.py                         # Main Streamlit entrypoint and navigation
│   ├── app_state.py                   # Shared session-state defaults, import/export, persistence helpers
│   ├── app_i18n.py                    # Language strings and i18n helpers
│   ├── app_ui.py                      # Shared UI helpers
│   ├── app_shell.py                   # Global page setup, cookies, CSS, language switcher
│   ├── app_pages_*.py                 # Calculator and content page implementations
│   └── assets/                        # Static assets such as flags and icons
├── requirements.txt
└── README.md
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Run locally

```bash
cd application
streamlit run app.py --server.port 8501
```

Then open the local Streamlit URL shown in the terminal.

## Deployment / local helper notes

- Main entrypoint: `application/app.py`
- Render helper script uses port `8880` and binds to `0.0.0.0`
- OCI helper script uses port `8880` and binds to `127.0.0.1`
- `runapp-oci.sh`, `runapp-render.sh`, and `requirements.lock.txt` are local helper files and are intentionally gitignored

## Disclaimer

This project is for educational planning and estimation only. It is not tax, legal, investment, or financial advice.
