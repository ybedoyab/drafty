from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import load_dotenv
from crewai_tools import VisionTool
from langchain_openai import ChatOpenAI
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Load environment variables from main project .env file
import sys
from pathlib import Path
# Go up from ai/ to the main project root
main_project_root = Path(__file__).parent.parent
env_file = main_project_root / ".env"
load_dotenv(env_file)

# Hard guard: ensure no global OpenAI base overrides (prevents LiteLLM from sending to Huawei)
for var in [
    "OPENAI_API_BASE",
    "OPENAI_BASE_URL",
    "OPENAI_API_TYPE",
    "LITELLM_BASE",
    "LITELLM_API_BASE",
    "OPENAI_BASE",
]:
    if var in os.environ:
        os.environ.pop(var, None)

# Use OpenAI for vision analysis
from langchain_openai import ChatOpenAI

# OpenAI LLM for vision (better image analysis)
openai_llm = ChatOpenAI(
    model=os.getenv("AI_OPENAI_MODEL", "gpt-4o"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1
)

# Vision tool using OpenAI
vision_tool = VisionTool()

# CAD generation handled directly in orchestrator; no CAD agent here

# (debug removed)

@CrewBase
class Draftycrew():
    """Draftycrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def visualizer(self) -> Agent:
        return Agent(
            config=self.agents_config['visualizer'], # type: ignore[index]
            verbose=True,
            tools=[vision_tool],
            llm=openai_llm,  # Use OpenAI for vision analysis
            allow_delegation=False
        )

    # CAD generator agent removed; generation done outside CrewAI

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def analyze_image(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_image'], # type: ignore[index]
        )

    # CAD task removed; orchestrator writes file directly

    @crew
    def crew(self) -> Crew:
        """Creates the Draftycrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
