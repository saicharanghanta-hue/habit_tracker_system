from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os


@CrewBase
class HabitTrackerCrew:
    """Habit Tracker CrewAI Pipeline"""

    agents_config = "crews/agents.yaml"
    tasks_config = "crews/tasks.yaml"

    @agent
    def analytics_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["analytics_strategist"],
            verbose=True,
        )

    @agent
    def habit_coach(self) -> Agent:
        return Agent(
            config=self.agents_config["habit_coach"],
            verbose=True,
        )

    @task
    def analyze_performance_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_performance_task"],
        )

    @task
    def generate_coaching_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_coaching_plan_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Habit Tracker crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

