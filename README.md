# Vettex: Autonomous Technical Due Diligence Agent

Vettex is an AI-powered intelligence tool designed for Venture Capitalists and technical analysts. It performs automated technical due diligence by investigating a company's claims against real-world data, engineering blogs, and developer sentiment.

Instead of simply summarizing a landing page, the agent treats marketing claims as hypotheses and attempts to verify them via live web searches using a **ReAct (Reasoning and Acting) loop**.

---

## 🚀 Features

* **Live Web Intelligence**: Integrated with **Tavily Search** to crawl GitHub, technical documentation, and forums.
* **Reasoning-First Approach**: Powered by **Google Gemini 3 Flash**, using a custom ReAct prompt that enforces skepticism and evidence-based analysis.
* **Real-time Progress Streaming**: Uses **Server-Sent Events (SSE)** to stream the agent's "Thoughts," "Actions," and "Observations" to a terminal-style UI.
* [cite_start]**Structured Technical Reports**: Automatically parses findings into a professional HTML report using **Pydantic** validation and **Jinja2** templates.

---

## 🛠️ Architecture



The system is built on a modern AI stack:
* **Backend**: FastAPI (Python)
* **Agent Framework**: LangChain (Classic & Core)
* **LLM**: Google Gemini 3 Flash
* **Search Engine**: Tavily AI
* **Frontend**: Tailwind CSS & Vanilla JS (for SSE streaming)

---

## 🚦 Getting Started

### 1. Environment Setup
Create a `.env` file in the root directory and add your API keys:
```env
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key

### 2. Installation
Install the dependencies listed in the requirements.txt:
```env
pip install -r requirements.txt

### 3. Run the Application
Start the server using Uvicorn:
```env
uvicorn main:app --reload
