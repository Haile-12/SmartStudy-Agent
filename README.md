# 🎓 SmartStudy Agent 
![Version](https://img.shields.io/badge/version-1.1.0-blue.svg?style=flat-square) 
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square) 
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat-square) 
![Framework](https://img.shields.io/badge/Agentic-CrewAI-orange.svg?style=flat-square)
![LLM](https://img.shields.io/badge/LLM-Gemini%20Flash-magenta.svg?style=flat-square)

> **"Transform Chaos into GPA."**

**SmartStudy Agent** is an enterprise-grade Multi-Agent System (MAS) designed to democratize elite-level academic coaching. By orchestrating a fleet of 6 specialized AI agents, it transforms raw, disorganized study materials (PDFs, PPTXs, Notes) into highly structured, actionable, and exam-focused learning roadmaps.

Powered by **CrewAI** and **Google Gemini** (Optimized for `flash-lite` efficiency), the system simulates a team of human experts—from a Professor summarizing notes to a Strategist planning your week—working in unison to guarantee your academic success.

---

## 🧠 System Architecture: Deep Dive

SmartStudy Agent is not just a chatbot wrapper; it is an orchestrated **Multi-Agent System (MAS)** that mimics a human study group.

### 🔄 The Logic Behind the Scenes

1.  **Strict Sequential Delegation**:
    *   Unlike chatty LLMs, agents here don't talk over each other.
    *   **Step 1**: `Summarizer` reads your 50-page PDF and compresses it to the "Golden Truth".
    *   **Step 2**: `Scheduler` takes that "Golden Truth" and time-blocks it. Without Step 1, Step 2 fails.
    *   **Step 3**: `QuizGenerator` looks at the "Golden Truth" to find weak spots.
    *   *Result*: Coherent, dependency-aware outputs.

2.  **State Management & Memory**:
    *   The backend (`backend/src/memory.py`) maintains a `SessionState`.
    *   As agents finish tasks, their outputs are stored in `state['context']`.
    *   The `StudyCoordinator` reads this final state to compile the report.

3.  **Real-Time Data Flow (SSE)**:
    *   **Backend**: `main.py` uses `queue.Queue` to capture `stdout` (print statements) from the CrewAI process.
    *   **Streamer**: A persistent `async` generator yields these logs to the frontend via `/generate-plan`.
    *   **Frontend**: `app.js` reads this stream chunk-by-chunk, updating the "Matrix-style" log in real-time.

4.  **Quota-Safe Engineering**:
    *   To allow this to run on **Free Tier** APIs, we stagger agent execution.
    *   We use `gemini-flash-lite` (low cost/high speed) for the heavy lifting (reading PDFs).
    *   We use `gemini-flash` (high reasoning) only for the final synthesis.

---

## 📂 Project Directory Structure

```plaintext
smart_study_agent/
├── ARCHITECTURE.md           # detailed architectural documentation
├── README.md                 # Project documentation (You are here)
├── backend/                  # Python FastAPI Backend
│   ├── .env                  # API Keys & Configuration
│   ├── main.py               # FastAPI Entry Point & WebSocket/SSE Logic
│   ├── requirements.txt      # Python Dependencies
│   ├── check_models.py       # Utility to verify Gemini models
│   ├── outputs/              # Artifact storage for generated reports
│   └── src/                  # Application Source Code
│       ├── agents.py         # Agent Factory & LLM Definitions
│       ├── crew.py           # CrewAI Orchestration & Kickoff Logic
│       ├── memory.py         # Custom Context & Session Memory Manager
│       ├── prompts.py        # System Prompts & Guardrails
│       ├── tasks.py          # Task Definitions & Expected Outputs
│       ├── tools.py          # Custom Tools (FileHandler, ArXivSearch)
│       └── config/           # YAML Configuration Files
│           ├── agents.yaml   # Agent Personas & Backstories
│           ├── tasks.yaml    # Detailed Task Instructions
│           └── settings.py   # Pydantic Settings Management
└── frontend/                 # High-Performance Vanilla JS Frontend
    ├── index.html            # Main Dashboard UI
    ├── app.js                # Frontend Logic (Streaming, Parsing, UI Updates)
    └── style.css             # Glassmorphism Theme & Responsive Design
```

---

## 🤖 The Agent Fleet

| Agent | Role | Model Strategy | Responsibility |
| :--- | :--- | :--- | :--- |
| **🧠 Note Summarizer** | *Knowledge Distiller* | `flash-lite` | Extracts high-yield concepts, formulas, and definitions from raw noise. Enforces strict Markdown structure. |
| **📅 Study Scheduler** | *Expert Strategist* | `flash-lite` | Creates a minute-by-minute, 7-day study plan with **Spaced Repetition** built-in. |
| **🔍 Resource Finder** | *Research Assistant* | `flash-lite` | Scours **arXiv** and academic repositories for high-quality supplementary materials using custom tools. |
| **❓ Quiz Generator** | *Examiner* | `flash-lite` | Drafts active recall questions targeting identified weak points and misconceptions. |
| **📈 Progress Analyst** | *Performance Coach* | `flash-lite` | Forecasts potential performance and assigns confidence scores (0-100%) to topics. |
| **📋 Coordinator** | *Orchestrator* | `flash` | Aggregates all outputs into a single, cohesive, formatted Markdown report, ensuring UI compatibility. |

> **Note on Efficiency**: Agents operate with `max_rpm=1` to strictly adhere to Gemini Free Tier quotas (15 RPM), preventing 429 errors.

---

## 🚀 Installation & Setup Guide

### Prerequisites
-   **Python 3.10** or higher.
-   A **Google Gemini API Key** (Get it free at [aistudio.google.com](https://aistudio.google.com)).

### 1. Environment Setup

Clone the repository and navigate to the backend:

```bash
cd smart_study_agent/backend
```

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

Install the required Python packages, including CrewAI, FastAPI, and document parsers:

```bash
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the `backend/` directory with your API key:

```ini
# backend/.env
GOOGLE_API_KEY=AIzaSy...YourKeyHere
```

### 4. Running the Application

**Start the Backend Server:**

```bash
# In backend/ directory with venv activated:
python main.py
```
*You will see: `Uvicorn running on http://127.0.0.1:8081`*

**Launch the Frontend:**
Simply open the `frontend/index.html` file in your preferred web browser (Chrome/Edge recommended).
*   Right-click `index.html` -> Open with -> Google Chrome.

---

## 💡 Usage Manual

### Generating a Study Plan

1.  **Input Data**:
    *   **Input Area**: Paste your lecture notes, syllabus, or raw text.
    *   **File Upload**: Click "Upload Document" to attach PDF, PPTX, or DOCX files. The text will be automatically extracted.
2.  **Topic Definition**: specific the main subject (e.g., "Reinforcement Learning").
3.  **Difficulty Setting**:
    *   **Beginner**: Focuses on fundamentals and broad overviews.
    *   **Expert**: Focuses on edge cases, derivations, and complex synthesis.
4.  **Execute**: Click **"Generate Study Plan"**.
5.  **Telemetry**: Watch the "Agent Process" panel. You will see real-time logs:
    *   `> Agent Note Summarizer started...`
    *   `> Tool ArXiv Search used...`

### Interacting with Results
*   **Summary Tab**: Read the High-Yield analysis.
*   **Roadmap Tab**: View your 7-Day table.
*   **Quiz Tab**: Test yourself (answers hidden/revealed).
*   **Resources Tab**: Click links to read actual academic papers.
*   **Download**: Click "Download Report" to get a beautifully formatted PDF version of the entire session.

---

## 🔧 Troubleshooting & FAQ

**Q: I see "429 Resource Exhausted" errors.**
*   **A**: You are hitting the Gemini Free Tier limit (15 requests/minute). The system has built-in rate limits (`max_rpm`), but if you trigger it, simply wait 60 seconds and try again.

**Q: The result boxes are empty?**
*   **A**: This usually means the backend crashed or the API key is invalid. Check the terminal where `main.py` is running for error logs.

**Q: Can I use GPT-4 instead?**
*   **A**: Yes. Update `backend/src/agents.py` to use `ChatOpenAI` and set `OPENAI_API_KEY` in your `.env`.

**Q: My PDF text isn't extracting.**
*   **A**: Ensure the PDF is text-selectable (OCR applied). Scanned images cannot be read by `pypdf` without Tesseract (not included to keep dependencies light).

---

## 📜 License

This project is licensed under the MIT License. You are free to use, modify, and distribute it.

---

---
## 🧪 Output Testimonials

![Output 1](image1.png)
![Output 2](image2.png)
---
*Built with ❤️ by Haile Tassew.*
