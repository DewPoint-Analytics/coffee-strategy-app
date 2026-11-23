<h1 align="center">☕ Coffee Shop Strategy · Business Dashboard</h1>

<p align="center">
  <a href="https://dewpoint-analytics.github.io/coffee-strategy-app/"><img alt="Open the app" src="https://img.shields.io/badge/Open%20the%20app-Streamlit-a8502e?style=for-the-badge&logo=streamlit&logoColor=white"></a>
  <a href="https://dewpoint-analytics.github.io/coffee-strategy-dashboard/?ref=streamlit-readme"><img alt="Full dashboard" src="https://img.shields.io/badge/%E2%98%95%20Full%20dashboard-15%20runs-2a1f19?style=for-the-badge"></a>
  <a href="https://dewpoint-analytics.github.io/3DCoffeeHub/?ref=streamlit-readme"><img alt="3D Coffee Hub" src="https://img.shields.io/badge/%F0%9F%8F%A0%203D%20Coffee%20Hub-step%20inside-6f9a4c?style=for-the-badge"></a>
</p>

<h3 align="center">15 runs of a coffee business, explored in Python.</h3>

An interactive dashboard built with **Python, Streamlit, pandas and Plotly** from my 15 runs of the Coffee Shop Inc. simulation (Sim Institute / Harvard Business Impact, October–November 2026).

## What you can explore

| Tab | What it shows |
|---|---|
| **Performance** | Five-year profit for every run as a share of its target, filterable by level |
| **Profit & loss** | Pick any Level 1 or 2 run: revenue, costs, profit and margin, year by year |
| **Level 3 growth** | Compare runs across Mature and Emerging markets: profit and store count by year |
| **Decision Lab** | 14 decisions ranked by their profit effect, with the evidence behind each |
| **Playbook** | Seven decision rules drawn from the results |

## Method

- Every figure in `data.json` was transcribed from the game's own result screens. Nothing is estimated.
- Later runs were paired with earlier ones, so a profit difference can be traced to the decision that changed. Comparisons marked "Descriptive" differed in more than one setting.
- The game is a simplification. Read the findings as decision principles, not forecasts.

## How it runs

The app runs entirely in your browser with [stlite](https://github.com/whitphx/stlite) (Streamlit on WebAssembly), hosted on GitHub Pages. No server and no third-party account access. The first visit takes about 20 seconds while Python loads; after that it is cached.

## Run it yourself

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Files

| File | Purpose |
|---|---|
| `index.html` | Starts the app in the browser (GitHub Pages) |
| `streamlit_app.py` | The app |
| `data.json` | Every figure used |
| `requirements.txt` | Python packages |
| `.streamlit/config.toml` | Colours and theme when run locally |
| `LICENSE` | Intellectual property notice (all rights reserved) |

## ©️ Intellectual property

© 2026 Shabnam Mohammed Sameer (DewPoint Analytics). All rights reserved. You may view the app and link to it; please do not copy or republish the analysis, design or code. See [LICENSE](LICENSE).
