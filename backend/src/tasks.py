import os
import yaml
from crewai import Task

class SmartStudyTasks:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'tasks.yaml')
        with open(config_path, 'r') as f:
            self.tasks_config = yaml.safe_load(f)

    def summarization_task(self, agent, notes, topic):
        return Task(
            config=self.tasks_config['summarization_task'],
            agent=agent,
            inputs={'notes': notes, 'topic': topic}
        )

    def planning_task(self, agent, notes, topic):
        return Task(
            config=self.tasks_config['planning_task'],
            agent=agent,
            inputs={'notes': notes, 'topic': topic}
        )

    def resource_finding_task(self, agent, topic):
        return Task(
            config=self.tasks_config['resource_finding_task'],
            agent=agent,
            inputs={'topic': topic}
        )

    def quiz_generation_task(self, agent, topic):
        return Task(
            config=self.tasks_config['quiz_generation_task'],
            agent=agent,
            inputs={'topic': topic}
        )

    def progress_analysis_task(self, agent, topic):
        return Task(
            config=self.tasks_config['progress_analysis_task'],
            agent=agent,
            inputs={'topic': topic}
        )
    
    def report_compilation_task(self, agent, context, topic):
        return Task(
            config=self.tasks_config['report_compilation_task'],
            agent=agent,
            context=context,
            inputs={'topic': topic}
        )
