"""CrewAI setup: defines visualizer agent and analysis task only."""
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import load_dotenv
from crewai_tools import VisionTool
from langchain_openai import ChatOpenAI
import os
import sys
from pathlib import Path

main_project_root = Path(__file__).parent.parent
env_file = main_project_root / ".env"
load_dotenv(env_file)

openai_llm = ChatOpenAI(
    model=os.getenv("AI_OPENAI_MODEL", "gpt-4o"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1
)

vision_tool = VisionTool()

@CrewBase
class Draftycrew():
    """Draftycrew crew."""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def visualizer(self) -> Agent:
        return Agent(
            config=self.agents_config['visualizer'], # type: ignore[index]
            verbose=True,
            tools=[vision_tool],
            llm=openai_llm,
            allow_delegation=False
        )

    @task
    def analyze_image(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_image'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Create the Draftycrew crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
