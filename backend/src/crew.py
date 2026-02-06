from crewai import Crew, Process
from .agents import (
    create_summarizer_agent, 
    create_scheduler_agent, 
    create_resource_finder_agent, 
    create_quiz_generator_agent, 
    create_progress_tracker_agent, 
    create_coordinator_agent,
    llm_group_b,
    quality_llm
)
from .tasks import SmartStudyTasks
from .config.settings import settings
from .memory import StudyMemory

import time
import uuid

class SmartStudyCrew:
    def __init__(self, topic, notes, session_id=None):
        self.topic = topic
        self.notes = notes
        self.tasks = SmartStudyTasks()
        
        self.session_id = session_id or f"study_{uuid.uuid4().hex[:8]}"
        self.memory = StudyMemory(self.session_id)
        self.memory.set_session_context(topic, notes, {"status": "initialized"})

    def on_task_completed(self, task_output):
        """Callback to wait between tasks for quota safety"""
        print(f"\n[QUOTA_SAFETY] Task completed. Waiting 15 seconds before next agent...")
        time.sleep(15)

    def run(self):
        # Initialize Agents
        summarizer = create_summarizer_agent()
        scheduler = create_scheduler_agent()
        finder = create_resource_finder_agent()
        quizzer = create_quiz_generator_agent()
        tracker = create_progress_tracker_agent()
        coordinator = create_coordinator_agent()

        # Initialize Tasks
        summary = self.tasks.summarization_task(summarizer, self.notes, self.topic)
        plan = self.tasks.planning_task(scheduler, self.notes, self.topic)
        resources = self.tasks.resource_finding_task(finder, self.topic)
        quiz = self.tasks.quiz_generation_task(quizzer, self.topic)
        analysis = self.tasks.progress_analysis_task(tracker, self.topic)

        report = self.tasks.report_compilation_task(
            coordinator, 
            [summary, plan, resources, quiz, analysis],
            self.topic
        )

        # Run the crew
        result = Crew(
            agents=[summarizer, scheduler, finder, quizzer, tracker, coordinator],
            tasks=[summary, plan, resources, quiz, analysis, report],
            process=Process.sequential,
            verbose=True,
            memory=False,
            embedder={
                "provider": "google-generativeai",
                "config": {
                    "model": "models/embedding-001"
                }
            },
            manager_llm=llm_group_b, # Use Account 2 for management
            task_callback=self.on_task_completed # Force wait between tasks
        ).kickoff(inputs={'topic': self.topic, 'notes': self.notes})
        
        # Store final result in custom memory
        self.memory.add_agent_output(
            agent_name="Study Coordinator",
            task="Final Report Compilation",
            output=str(result)
        )
        
        return result, self.memory

