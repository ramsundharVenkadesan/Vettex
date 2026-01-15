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

# 🛠 Troubleshooting: SSL Certificate Verification & Agent Resiliency

While running the **Vettex Technical Due Diligence Agent**, you may encounter a connection error when the agent attempts to use the search tool. This document explains why this happens and how the system's architecture handles it.

---

## 🚨 The Error: SSL Certificate Verification Failed

### **Error Log**
`ClientConnectorCertificateError: ... [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1028)`

### **Description**
This error occurs because the local Python environment (specifically the `aiohttp` library used by `langchain_tavily`) cannot verify the identity of the remote server at `api.tavily.com`. 

**Key reasons for this failure:**
* **Missing CA Bundle:** Your machine lacks the local list of Certificate Authorities (CA) required to validate the SSL/TLS certificate provided by the API.
* **macOS Configuration:** Python on macOS often does not automatically link to the system's root certificates, requiring a manual installation of the cert bundle.

---

## 🧠 Agent Self-Correction (ReAct Framework)

One of the defining features of this agent is its **resiliency**. Even when the `TavilySearch` tool fails due to an SSL error, the application does not crash. Instead, it utilizes the **ReAct (Reasoning and Acting)** loop to adapt.

### **How it Works**

1.  **Error as Observation:** The `AgentExecutor` in `main.py` is configured with `handle_parsing_errors=True`. When the tool fails, the framework catches the exception and returns the error string to the LLM as an **Observation**.
2.  **Reasoning Loop:** The LLM (Gemini) reads the error in its "scratchpad". It recognizes that the search action failed and reflects on this in its next **Thought** step.
3.  **Graceful Degradation:** According to the `REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS`, the agent is directed to use tools for proof but avoid hallucinations. 
    * If a search fails, the agent may attempt to answer based on its internal training data (Internal Knowledge Fallback).
    * It will prioritize providing a high-level technical verdict over crashing, while noting that live data retrieval was limited.



---

## ⚠️ Disclaimer

Vettex is an assistive due diligence tool and should not replace professional investment advice.

---

## 📄 License

MIT License
