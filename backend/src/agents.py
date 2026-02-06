import os
import time
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools import AcademicSearchTool, FileHandlerTool

# --- Environment Lockdown (Nexus AI Strict Mode) ---
os.environ["OPENAI_API_KEY"] = "none"
os.environ["OPENAI_API_BASE"] = "http://localhost:1" # Kill switch
os.environ["LITELLM_LOGGING"] = "False"
os.environ["CREWAI_SKIP_TELEMETRY"] = "true"
# Force LiteLLM to use native google calls instead of openai proxies
os.environ["LITELLM_MODE"] = "native" 

class QuotaSafeLLM(ChatGoogleGenerativeAI):
    """Nexus AI Style: Wait for next minute on 429 errors"""
    def _generate(self, *args, **kwargs):
        while True:
            try:
                return super()._generate(*args, **kwargs)
            except Exception as e:
                err = str(e).upper()
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    print(f"\n[QUOTA_ALERT] Rate limit reached. Waiting 70s for 'Next Minute' reset (Nexus Logic)...")
                    time.sleep(70)
                else:
                    raise e

    def invoke(self, *args, **kwargs):
        while True:
            try:
                return super().invoke(*args, **kwargs)
            except Exception as e:
                err = str(e).upper()
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    print(f"\n[QUOTA_ALERT] Rate limit reached. Waiting 70s for 'Next Minute' reset (Nexus Logic)...")
                    time.sleep(70)
                else:
                    raise e


# --- Double Key / Double Model Distribution ---
api_key_1 = os.getenv("GOOGLE_API_KEY")
api_key_2 = os.getenv("GOOGLE_API_KEY_2") or api_key_1

# Account 1: Gemini 2.5 Flash-Lite (High Resilience - 1,000 RPD)
llm_acc1_flash = QuotaSafeLLM(
    model="gemini-2.5-flash-lite",
    google_api_key=api_key_1,
    temperature=0.1
)

# Account 2: Gemini 2.5 Pro (Expert Analysis - 25 RPD)
llm_acc2_pro = QuotaSafeLLM(
    model="gemini-2.5-flash-lite",
    google_api_key=api_key_2,
    temperature=0.4
)




# Distribution Variables (Nexus Pattern)
llm_group_a = llm_acc1_flash  # Summarizer, Finder, Tracker
llm_group_b = llm_acc2_pro    # Scheduler, Quizzer, Coordinator
quality_llm = llm_acc2_pro




def create_summarizer_agent() -> Agent:
    """Note Summarizer - Extracts high-yield exam content"""
    return Agent(
        role="Note Summarizer",
        goal=(
            "Transform raw study materials about {topic} into concise, high-yield summaries "
            "highlighting key concepts, definitions, formulas, and exam-critical information"
        ),
        backstory=(
            "Former senior textbook editor for Pearson and McGraw-Hill with 15+ years of experience "
            "distilling complex academic subjects into memorable, exam-focused content. "
            "Master of identifying high-yield information while eliminating cognitive clutter. "
            "Specializes in creating summaries that maximize retention and exam performance."
        ),
        llm=llm_group_a, # Distribution Group A (Key 1 / gemini-pro)
        tools=[FileHandlerTool()],
        allow_delegation=False,
        verbose=True,
        memory=False,
        max_rpm=1,
        max_iter=3 # Prevent quota burning
    )

def create_scheduler_agent() -> Agent:
    """Study Scheduler - Creates optimized study plans"""
    return Agent(
        role="Study Scheduler",
        goal=(
            "Create optimal daily/weekly study schedules for {topic} that balance depth, "
            "retention, and exam preparation with realistic time allocation"
        ),
        backstory=(
            "Certified learning strategist who has designed study plans for 10,000+ students. "
            "Expert in spaced repetition, Pomodoro technique, and cognitive load optimization. "
            "Known for creating achievable schedules that maximize learning efficiency without burnout."
        ),
        llm=llm_group_b, # Distribution Group B (Key 2 / gemini-1.5-pro)
        allow_delegation=False,
        verbose=True,
        memory=False,
        max_rpm=1,
        max_iter=3
    )

def create_resource_finder_agent() -> Agent:
    """Resource Finder - Locates quality learning materials"""
    return Agent(
        role="Resource Finder",
        goal=(
            "Discover and curate high-quality, free academic resources for {topic} including "
            "research papers, video lectures, and practice problems"
        ),
        backstory=(
            "Digital librarian and academic research specialist with deep knowledge of open-access educational resources. "
            "Expert at finding MIT OpenCourseWare, Khan Academy, arXiv papers, and university lecture notes. "
            "Prioritizes credible, peer-reviewed sources over commercial content."
        ),
        llm=llm_group_a, # Distribution Group A (Key 1 / gemini-pro)
        tools=[AcademicSearchTool()],
        allow_delegation=False,
        verbose=True,
        memory=False,
        max_rpm=1,
        max_iter=3
    )

def create_quiz_generator_agent() -> Agent:
    """Quiz Generator - Creates challenging practice questions"""
    return Agent(
        role="Quiz Generator",
        goal=(
            "Design challenging, exam-style practice questions for {topic} that expose common "
            "misconceptions and test deep understanding"
        ),
        backstory=(
            "Former AP exam question writer and Kaplan Test Prep instructor with expertise in creating "
            "diagnostic assessments. Specializes in questions that identify knowledge gaps and encourage "
            "active recall. Master of Bloom's taxonomy and higher-order thinking questions."
        ),
        llm=llm_group_b, # Distribution Group B (Key 2 / gemini-1.5-pro)
        allow_delegation=False,
        verbose=True,
        memory=False,
        max_rpm=1,
        max_iter=3
    )

def create_progress_tracker_agent() -> Agent:
    """Progress Tracker - Analyzes learning performance"""
    return Agent(
        role="Progress Tracker",
        goal=(
            "Analyze student performance on {topic}, identify knowledge gaps, and recommend "
            "targeted improvement strategies"
        ),
        backstory=(
            "Educational data scientist with background in learning analytics and adaptive learning systems. "
            "Expert at diagnosing misconceptions from quiz performance and providing actionable feedback. "
            "Uses evidence-based approaches to measure confidence and mastery."
        ),
        llm=llm_group_a, # Distribution Group A (Key 1 / gemini-pro)
        allow_delegation=False,
        verbose=True,
        memory=False,
        max_rpm=1,
        max_iter=3
    )

def create_coordinator_agent() -> Agent:
    """Study Coordinator - Orchestrates the study workflow"""
    return Agent(
        role="Study Coordinator",
        goal=(
            "Synthesize insights from all agents into a comprehensive, actionable study plan for {topic} "
            "that integrates summaries, schedules, quizzes, resources, and progress tracking"
        ),
        backstory=(
            "Senior academic advisor and curriculum designer with a PhD in Educational Psychology. "
            "Expert at integrating multiple learning modalities into cohesive study programs. "
            "Known for creating holistic learning experiences that address cognitive, practical, and motivational needs."
        ),
        llm=llm_group_b, # Distribution Group B (Key 2 / gemini-1.5-pro)
        allow_delegation=False,
        verbose=True,
        memory=False,
        max_rpm=1,
        max_iter=5 # Master needs more thought
    )
