from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dev_aem_crew_sys.tools.vision_tool import VisionTool
from dev_aem_crew_sys.tools.file_writer_tool import FileWriterTool
from dev_aem_crew_sys.tools.file_reader_tool import FileReaderTool
from dev_aem_crew_sys.tools.aem_file_writer_tool import AEMFileWriterTool
from dev_aem_crew_sys.tools.maven_tool import MavenTool
from dev_aem_crew_sys.tools.user_interaction_tool import UserInteractionTool
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class DevAemCrewSys():
    """DevAemCrewSys crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def webdesigner(self) -> Agent:
        # Create LLM instance for Claude
        llm = LLM(
            model="anthropic/claude-3-5-sonnet-20241022",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        return Agent(
            config=self.agents_config['webdesigner'], # type: ignore[index]
            verbose=True,
            tools=[VisionTool()],
            llm=llm
        )

    @agent
    def component_developer(self) -> Agent:
        # Create LLM instance for Claude
        llm = LLM(
            model="anthropic/claude-3-5-sonnet-20241022",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        return Agent(
            config=self.agents_config['component_developer'], # type: ignore[index]
            verbose=True,
            tools=[FileWriterTool()],
            llm=llm
        )

    @agent
    def aem_developer(self) -> Agent:
        # Create LLM instance for Claude
        llm = LLM(
            model="anthropic/claude-3-5-sonnet-20241022",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        return Agent(
            config=self.agents_config['aem_developer'], # type: ignore[index]
            verbose=True,
            tools=[FileReaderTool(), AEMFileWriterTool(), MavenTool(), UserInteractionTool()],
            llm=llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def design_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_analysis_task'], # type: ignore[index]
            output_file='design_analysis.txt'
        )

    @task
    def component_listing_task(self) -> Task:
        return Task(
            config=self.tasks_config['component_listing_task'], # type: ignore[index]
            output_file='component_list.txt'
        )

    @task
    def component_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['component_creation_task'], # type: ignore[index]
            output_file='component_summary.txt'
        )

    @task
    def aem_component_list_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_component_list_task'], # type: ignore[index]
            output_file='aem_component_selection.txt'
        )

    @task
    def aem_component_conversion_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_component_conversion_task'], # type: ignore[index]
            output_file='aem_component_files.txt'
        )

    @task
    def aem_build_deploy_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_build_deploy_task'], # type: ignore[index]
            output_file='aem_build_log.txt'
        )

    @task
    def aem_testing_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_testing_task'], # type: ignore[index]
            output_file='aem_testing_report.txt'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DevAemCrewSys crew for HTML component creation and AEM conversion"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=[self.webdesigner(), self.component_developer(), self.aem_developer()],
            tasks=[
                # First phase: Design analysis and HTML component creation
                self.design_analysis_task(),
                self.component_listing_task(),
                self.component_creation_task(),
                # Second phase: AEM conversion and deployment
                self.aem_component_list_task(),
                self.aem_component_conversion_task(),
                self.aem_build_deploy_task(),
                self.aem_testing_task()
            ],
            process=Process.sequential,
            verbose=True,
        )

    
