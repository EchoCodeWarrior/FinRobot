
# FinRobot Agentic Analyst /// Neo-Brutalism Edition

A Streamlit-based financial analysis application powered by **FinRobot**, **AutoGen**, and **Google Gemini**. Designed with a Neo-Brutalist aesthetic for a bold user experience.

## SETUP

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Application**:
   ```bash
   streamlit run app.py
   ```

## REQUIRED API KEYS

You need the following API keys to run the agents. Enter them in the app sidebar.

| API Key | Service | Purpose | Get it here |
| :--- | :--- | :--- | :--- |
| **GOOGLE_API_KEY** | Google Gemini | LLM Model (Gemini 1.5 Pro) | [Google AI Studio](https://aistudio.google.com/) |
| **FMP_API_KEY** | Financial Modeling Prep | Financial Statements & 10-K Data | [FMP Developer](https://site.financialmodelingprep.com/) |
| **FINNHUB_API_KEY** | Finnhub | Stock Basics & News | [Finnhub Dashboard](https://finnhub.io/dashboard) |

## FEATURES

- **Market Forecaster**: Predict stock movements with a focus on Indian Markets (NSE/BSE).
- **Annual Report Analyzer**: Deep dive into financial health using FMP data.
