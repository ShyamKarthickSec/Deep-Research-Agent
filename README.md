---
title: Shyams_Deep_Research_Assistant
app_file: app.py
sdk: gradio
sdk_version: 5.34.2
---
#  Shyam's Deep Research Agent

An agentic, multi-stage research assistant that transforms a vague user query into a high-quality, deeply researched report by combining:

- Intelligent clarifying questions  
- Automated search planning  
- Parallel web research  
- Structured long-form synthesis  
- Optional email delivery  
- A clean ChatGPT-like UI built with Gradio  

This project demonstrates a real-world agent orchestration pipeline, not a single-prompt LLM call.

---

##  Key Features
-  **Clarifier Agent** – Asks exactly 4 targeted questions to refine the research scope  
-  **Planner Agent** – Designs an optimal web search plan  
-  **Search Agent** – Executes parallel web searches using tool-calling  
-  **Writer Agent** – Synthesizes results into a detailed Markdown report (1000+ words)  
-  **Email Agent** – Sends the final report as a clean HTML email  
-  **Research Manager** – Orchestrates the full agent pipeline with tracing  
-  **Interactive UI** – ChatGPT-style Gradio interface with stateful refinement  
-  **Tracing Enabled** – Full OpenAI trace IDs for debugging and observability  

---

##  Architecture Overview
```
User Query
   │
   ▼
Clarifier Agent ──► 4 Clarifying Questions
   │
   ▼
Refined Prompt
   │
   ▼
Planner Agent ──► Search Plan
   │
   ▼
Search Agent (parallel)
   │
   ▼
Writer Agent ──► Long-form Markdown Report
   │
   ▼
Email Agent (optional)
```
This separation of concerns makes the system modular, testable, and extensible.

---

##  Project Structure
```
.
├── deep_research.py        # Gradio UI + user interaction flow
├── research_manager.py     # Orchestrates the full research pipeline
├── clarifier_agent.py      # Generates clarifying questions
├── planner_agent.py        # Plans web searches
├── search_agent.py         # Executes web searches via tool calling
├── writer_agent.py         # Writes the final research report
├── email_agent.py          # Emails the report using Resend
├── .env                    # API keys (not committed)
└── README.md
```

---

##  Agents Explained
### 1) Clarifier Agent
- Generates exactly four focused clarifying questions to improve research quality.  
- Built with Pydantic output validation; guaranteed structured output.  
- Automatic fallback questions if the agent fails.  
- 📄 Source: `clarifier_agent.py` (`clarifier_agent`)

### 2) Planner Agent
- Creates a search strategy tailored to the refined query.  
- Produces reasoned search terms; controls number of searches explicitly.  
- Ensures coverage and relevance.  
- 📄 Source: `planner_agent.py` (`planner_agent`)

### 3) Search Agent
- Executes web searches using OpenAI’s `WebSearchTool`.  
- Parallel execution; concise, synthesis-ready summaries.  
- Tool-forced invocation (no hallucinated browsing).  
- 📄 Source: `search_agent.py` (`search_agent`)

### 4) Writer Agent
- Synthesizes all findings into a long-form Markdown report.  
- Generates an outline before writing; produces 5–10 pages of structured content.  
- Returns: short summary, full Markdown report, follow-up research questions.  
- 📄 Source: `writer_agent.py` (`writer_agent`)

### 5) Email Agent
- Formats the report into HTML and sends it via Resend.  
- Uses tool calling (`@function_tool`), clean HTML formatting, robust error handling.  
- 📄 Source: `email_agent.py` (`email_agent`)

### 6) Research Manager
- The control plane of the system.  
- Coordinates all agents; runs searches concurrently with `asyncio`.  
- Emits OpenAI trace IDs for observability; streams progress updates to the UI.  
- 📄 Source: `research_manager.py` (`research_manager`)

---

##  User Interface
- Built with Gradio, styled for a subtle ChatGPT-like dark theme.  
- Flow:
  1. Enter research query  
  2. Answer clarifying questions  
  3. Run deep research  
  4. View streamed progress + final report  
  5. Reset and start over  
- 📄 Source: `app.py` (`app`)

---

##  Getting Started
### 1) Install Dependencies
```bash
pip install gradio python-dotenv resend openai-agents
```
Ensure your environment supports async execution (Python 3.10+ recommended).

### 2) Set Environment Variables
Create a `.env` file:
```
OPENAI_API_KEY=your_openai_key
RESEND_API_KEY=your_resend_key
```

### 3) Run the App
```bash
python app.py
```
The UI will launch in your browser at:
```
http://127.0.0.1:7860
```

---

##  Example Use Cases
- Academic literature reviews  
- Market & competitive research  
- Policy and regulation analysis  
- Technical deep dives  
- Startup or investment research  
- Long-form blog or whitepaper drafts  

---

##  Why This Project Is Different
- ✔ Not a single-prompt chatbot  
- ✔ True agentic decomposition  
- ✔ Deterministic structured outputs  
- ✔ Parallel research execution  
- ✔ Production-grade orchestration  
- ✔ UI + backend + delivery pipeline  

This is portfolio-grade agent engineering, not a demo.

---

##  Future Pipeline Integrations:
- Add citation extraction & reference linking  
- Plug in vector databases for memory  
- Replace search tool with custom crawlers  
- Add PDF / DOCX export  
- Add multi-language support  
- Add evaluation / confidence scoring agent  

---

##  Author
Shyam Karthick
