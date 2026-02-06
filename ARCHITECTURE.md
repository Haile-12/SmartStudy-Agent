# NexusStudy Agent Architecture

## Overview
NexusStudy is an advanced multi-agent system designed to orchestrate academic success through hierarchical task delegation and specialized AI agents. It leverages the CrewAI framework and Google's Gemini models to provide high-yield study materials and roadmap orchestration.

## The Agent Fleet

### 1. Study Coordinator (Manager)
- **Role**: Orchestrates the entire session.
- **Responsibility**: Delegating tasks to specialists, aggregating results, and ensuring the final report meets the user's academic goals.
- **Strategy**: Hierarchical coordination.

### 2. Note Summarizer
- **Role**: Knowledge Distillation.
- **Goal**: Transform raw materials into high-yield, exam-critical summaries.
- **Focus**: Key concepts, formulas, and definitions.

### 3. Study Scheduler
- **Role**: Learning Strategist.
- **Goal**: Create optimized 7-day study plans.
- **Concepts**: Spaced repetition, cognitive load management.

### 4. Resource Finder
- **Role**: Research Assistant.
- **Goal**: Discover supplementary academic resources via arXiv and university repositories.
- **Tools**: `AcademicSearchTool` (arXiv integration).

### 5. Quiz Generator
- **Role**: Active Recall Expert.
- **Goal**: Craft practice questions that target common misconceptions and test deep understanding.

### 6. Progress Tracker
- **Role**: Learning Scientist.
- **Goal**: Analyze confidence levels, identify knowledge gaps, and suggest targeted improvements.

## Technical Stack
- **Backend**: FastAPI (Python 3.10+)
- **Agent Orchestration**: CrewAI
- **LLM**: Google Gemini (via LiteLLM prefix `gemini/`)
- **Frontend**: Vanilla JS, HTML5, CSS3 (Glassmorphism design)
- **Research API**: arXiv

## Design Decisions
1. **Hierarchical Process**: We use a manager agent instead of a linear process to ensure complex topics are broken down logically and results are refined by a central coordinator.
2. **Stateless Logic**: To maintain performance and avoid external vector database dependencies, we prioritize high-context windows and shared task context over persistent vector memory.
3. **Gemini First**: The architecture is optimized specifically for Gemini's API structure, including dummy OpenAI key injection to satisfy legacy library dependencies.
4. **Stream-First UI**: The backend uses Event Streaming to provide real-time "telemetry" logs to the frontend, showing the agents "thinking" in real-time.
