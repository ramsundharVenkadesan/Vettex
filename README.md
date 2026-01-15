# Vettex | Autonomous Technical Due Diligence Agent

Vettex is a specialized AI agent designed for Venture Capital analysts to conduct **rapid, evidence-based technical due diligence**. By leveraging LangChain’s ReAct framework and Google Gemini, it cross-references marketing claims against **live technical data** (GitHub, documentation, engineering blogs) to assess a company’s true technical defensibility.

---

## 🚀 Features

- **Live Web Research**  
  Uses Tavily Search to find real-time technical proof and supporting evidence.

- **Streaming Logs**  
  Watch the agent’s internal *Thoughts* and *Actions* stream live in a terminal-style UI.

- **Structured Analysis**  
  Automatically generates a detailed report covering:
  - Value Proposition  
  - Technical Architecture  
  - Developer Sentiment  
  - Red Flags & Risks  
  - Final Investment Verdict

- **Modern UI**  
  Built with FastAPI, Tailwind CSS, and Jinja2 templates for a clean, responsive experience.

---

## 🛠️ Prerequisites

Before running the application, ensure you have:

- **Python 3.9+** installed
- API keys for the following services:
  - **Google Gemini** – powers the agent’s reasoning  
  - **Tavily AI** – enables real-time web search

---

## 📥 Installation

```bash
cd vettex-due-diligence
python -m venv venv
```

Activate the virtual environment:

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

---

## 🏃 Running the Application

```bash
uvicorn main:app --reload
```

Open your browser:

```
http://127.0.0.1:8000
```

---

## 📖 How to Use

1. Enter the company name and official website URL  
2. Click **Start Technical Audit**  
3. Watch live agent reasoning in the terminal UI  
4. Review the generated Technical Intelligence Report

---

## 🏗️ Project Structure

```
vettex-due-diligence/
│
├── main.py
├── prompt.py
├── schema.py
├── requirements.txt
├── templates/
│   ├── index.html
│   └── report.html
└── .env
```

---

## 🧠 Core Technologies

- LangChain (ReAct)
- Google Gemini
- Tavily Search
- FastAPI
- Tailwind CSS
- Jinja2

---

## ⚠️ Disclaimer

Vettex is an assistive due diligence tool and should not replace professional investment advice.

---

## 📄 License

MIT License
