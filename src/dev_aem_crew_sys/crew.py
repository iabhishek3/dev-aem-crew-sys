from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dev_aem_crew_sys.tools.vision_tool import VisionTool
from dev_aem_crew_sys.tools.file_writer_tool import FileWriterTool
from dev_aem_crew_sys.tools.file_reader_tool import FileReaderTool
from dev_aem_crew_sys.tools.directory_list_tool import DirectoryListTool
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
    def visual_strategist(self) -> Agent:
        # Create LLM instance for Claude with retry settings
        # Use MODEL from .env or default to claude-3-5-sonnet-20241022
        model_name = os.getenv("MODEL", "anthropic/claude-3-5-sonnet-20241022")
        if not model_name.startswith("anthropic/"):
            model_name = f"anthropic/{model_name}"

        llm = LLM(
            model=model_name,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            timeout=120,  # 2 minute timeout
            max_retries=5  # Retry up to 5 times on failure
        )

        return Agent(
            config=self.agents_config['visual_strategist'], # type: ignore[index]
            verbose=True,
            tools=[VisionTool()],
            llm=llm
        )

    @agent
    def ui_architect(self) -> Agent:
        # Create LLM instance for Claude with retry settings
        model_name = os.getenv("MODEL", "anthropic/claude-3-5-sonnet-20241022")
        if not model_name.startswith("anthropic/"):
            model_name = f"anthropic/{model_name}"

        llm = LLM(
            model=model_name,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            timeout=120,  # 2 minute timeout
            max_retries=5  # Retry up to 5 times on failure
        )

        return Agent(
            config=self.agents_config['ui_architect'], # type: ignore[index]
            verbose=True,
            tools=[FileWriterTool()],
            llm=llm
        )

    @agent
    def aem_alchemist(self) -> Agent:
        # Use OpenAI for AEM agent (more stable for complex tasks)
        # Falls back to Anthropic if AEM_MODEL not set
        aem_model = os.getenv("AEM_MODEL", "")

        if aem_model and (aem_model.startswith("gpt") or aem_model.startswith("openai/")):
            # Use OpenAI for AEM agent
            if not aem_model.startswith("openai/"):
                aem_model = f"openai/{aem_model}"

            llm = LLM(
                model=aem_model,
                api_key=os.getenv("OPENAI_API_KEY"),
                timeout=120,  # 2 minute timeout
                max_retries=5  # Retry up to 5 times on failure
            )
        else:
            # Fallback to Anthropic
            model_name = os.getenv("MODEL", "anthropic/claude-3-5-sonnet-20241022")
            if not model_name.startswith("anthropic/"):
                model_name = f"anthropic/{model_name}"

            llm = LLM(
                model=model_name,
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                timeout=120,  # 2 minute timeout
                max_retries=5  # Retry up to 5 times on failure
            )

        return Agent(
            config=self.agents_config['aem_alchemist'], # type: ignore[index]
            verbose=True,
            tools=[DirectoryListTool(), FileReaderTool(), AEMFileWriterTool(), MavenTool(), UserInteractionTool()],
            llm=llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def design_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_analysis_task'], # type: ignore[index]
            output_file='output-visual_strategist/design_analysis.md'
        )

    @task
    def component_listing_task(self) -> Task:
        return Task(
            config=self.tasks_config['component_listing_task'], # type: ignore[index]
            output_file='output-ui_architect/component_list.md'
        )

    @task
    def component_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['component_creation_task'], # type: ignore[index]
            output_file='output-ui_architect/component_summary.txt'
        )

    @task
    def aem_component_list_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_component_list_task'], # type: ignore[index]
            output_file='output-aem_alchemist/aem_component_selection.txt'
        )

    @task
    def aem_component_conversion_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_component_conversion_task'], # type: ignore[index]
            output_file='output-aem_alchemist/aem_component_files.txt'
        )

    @task
    def aem_build_deploy_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_build_deploy_task'], # type: ignore[index]
            output_file='output-aem_alchemist/aem_build_log.txt'
        )

    @task
    def aem_testing_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_testing_task'], # type: ignore[index]
            output_file='output-aem_alchemist/aem_testing_report.txt'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DevAemCrewSys crew for HTML component creation and AEM conversion"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=[self.visual_strategist(), self.ui_architect(), self.aem_alchemist()],
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

    
