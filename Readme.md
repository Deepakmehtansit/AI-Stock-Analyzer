# 🏦 AI Equity Research Agent

An intelligent financial analysis platform that leverages AI agents to perform deep fundamental and technical research on global stocks. [cite_start]The application provides real-time insights, valuation metrics, and technical trends through a professional-grade web interface[cite: 26, 32, 33, 71].

## 🚀 Features

* [cite_start]**Automated Fundamental Analysis**: Evaluates post-merger dynamics, asset quality (GNPA), credit growth, and valuation metrics like P/E Ratios[cite: 4, 6, 9, 10, 42].
* [cite_start]**Technical Trend Monitoring**: Analyzes price action relative to 50-Day Moving Averages and tracks momentum using the Relative Strength Index (RSI)[cite: 13, 15, 52, 58].
* [cite_start]**Risk Assessment**: Identifies critical risks such as deposit accrual lags, regulatory changes, and index weightage shifts[cite: 18, 20, 21, 61].
* [cite_start]**Interactive UI**: A streamlined Streamlit interface for entering tickers and custom research queries[cite: 27, 29, 31, 55].
* [cite_start]**Exportable Reports**: Generate and download comprehensive equity research reports as plain text files directly from the browser[cite: 69].

---

## 🛠️ Tech Stack

### **Core Frameworks**
* [cite_start]**LangChain & LangGraph**: Orchestrates the AI agent's reasoning, checkpointing, and tool-calling capabilities[cite: 1, 72].
* [cite_start]**OpenAI GPT Models**: Powers the core analytical engine for generating research insights[cite: 1, 72].

### **Data & Finance**
* [cite_start]**yfinance**: Fetches real-time and historical market data[cite: 1, 72].
* [cite_start]**Pandas & NumPy**: Handles data manipulation and numerical analysis[cite: 1, 72].

### **Frontend**
* [cite_start]**Streamlit**: Provides the interactive web dashboard and report visualization[cite: 1, 72].

---

## 📦 Installation & Setup

### **1. Clone the Repository**
```bash
git clone <your-repository-url>
cd ai-equity-research-agent

pip install -r requirements.txt

OPENAI_API_KEY=your_openai_api_key_here

streamlit run app.py

The application will be accessible at http://localhost:8501