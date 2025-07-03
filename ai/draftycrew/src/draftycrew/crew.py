from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import load_dotenv
from crewai_tools import VisionTool
from langchain_openai import ChatOpenAI
from draftycrew.tools import OpenSCADValidator, OpenSCADKnowledgeTool
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Load environment variables
load_dotenv()

# Use local vision tool for local files
vision_tool = VisionTool()

# Initialize OpenSCAD tools
openscad_validator = OpenSCADValidator()
openscad_knowledge = OpenSCADKnowledgeTool()

# Initialize LLMs
gpt4o_llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,
    api_key=os.getenv("OPENAI_API_KEY")
)

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
            llm=gpt4o_llm,
            allow_delegation=False
        )

    @agent
    def cad_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['cad_generator'], # type: ignore[index]
            verbose=True,
            tools=[openscad_knowledge, openscad_validator],  # Add OpenSCAD tools
            llm=gpt4o_llm,  # Using GPT-4o for CAD generation
            allow_delegation=False
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def analyze_image(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_image'], # type: ignore[index]
        )

    @task
    def generate_cad(self) -> Task:
        return Task(
            config=self.tasks_config['generate_cad'], # type: ignore[index]
            output_file='generated_cad_script.scad'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Draftycrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
