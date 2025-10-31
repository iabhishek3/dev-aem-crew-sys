from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff
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
import time
import shutil
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

def task_delay_callback(output):
    """
    Production-ready callback to add delay between tasks.
    Helps prevent API rate limiting and overload errors.
    """
    print(f"\n⏳ Task completed. Waiting 3 seconds before next task to prevent API overload...\n")
    time.sleep(3)  # 3-second delay between tasks
    return output

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

    @before_kickoff
    def cleanup_output_directories(self, inputs):
        """
        Clean up previous output directories before starting a new crew run.
        This ensures fresh output for each execution.
        Only cleans directories that are actually used in the current workflow.
        """
        output_dirs = [
            'output-visual_strategist',  # Used: design_analysis.json
            'output-aem_alchemist',      # Used: task output logs (01-07)
            # Note: output-ui_architect is NOT used in direct AEM workflow
            # Note: output-aem-component is NOT used (files written directly to AEM project)
        ]

        print("\n🧹 Cleaning up previous output directories...")
        for dir_path in output_dirs:
            if os.path.exists(dir_path):
                try:
                    shutil.rmtree(dir_path)
                    print(f"   ✓ Removed: {dir_path}")
                except Exception as e:
                    print(f"   ⚠ Warning: Could not remove {dir_path}: {e}")

        print("✨ Cleanup complete. Starting fresh run...\n")
        return inputs

    @agent
    def visual_strategist(self) -> Agent:
        # Create LLM instance for Claude with retry settings
        # Use MODEL from .env or default to latest Sonnet 4.5 (September 2025)
        model_name = os.getenv("MODEL", "anthropic/claude-sonnet-4-5-20250929")
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
        model_name = os.getenv("MODEL", "anthropic/claude-sonnet-4-5-20250929")
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
        # Use MODEL from .env or default to Sonnet 4.5
        model_name = os.getenv("MODEL", "anthropic/claude-sonnet-4-5-20250929")
        if not model_name.startswith("anthropic/"):
            model_name = f"anthropic/{model_name}"

        llm = LLM(
            model=model_name,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            timeout=180,  # 3 minute timeout per task (increased from 120)
            max_retries=10  # More retries for API overload handling (increased from 3)
        )

        return Agent(
            config=self.agents_config['aem_alchemist'], # type: ignore[index]
            verbose=True,
            tools=[
                DirectoryListTool(),
                FileReaderTool(),
                AEMFileWriterTool()  # Using AEMFileWriterTool to write directly to AEM project
            ],
            llm=llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def design_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_analysis_task'], # type: ignore[index]
            output_file='output-visual_strategist/design_analysis.json',
            callback=task_delay_callback  # Add delay after task
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
            output_file='output-aem_alchemist/aem_component_files.txt',
            context=[self.design_analysis_task()]  # Pass JSON from Visual Strategist
        )

    # Multi-task breakdown for AEM component generation
    @task
    def aem_component_definition_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_component_definition_task'], # type: ignore[index]
            output_file='output-aem_alchemist/01_component_definition.txt',
            context=[self.design_analysis_task()],
            callback=task_delay_callback  # Add delay after task
        )

    @task
    def aem_htl_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_htl_generation_task'], # type: ignore[index]
            output_file='output-aem_alchemist/02_htl_template.txt',
            context=[self.design_analysis_task(), self.aem_component_definition_task()],
            callback=task_delay_callback  # Add delay after task
        )

    @task
    def aem_sling_model_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_sling_model_generation_task'], # type: ignore[index]
            output_file='output-aem_alchemist/03_sling_model.txt',
            context=[self.design_analysis_task(), self.aem_htl_generation_task()],
            callback=task_delay_callback  # Add delay after task
        )

    @task
    def aem_dialog_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_dialog_generation_task'], # type: ignore[index]
            output_file='output-aem_alchemist/04_dialog.txt',
            context=[self.design_analysis_task(), self.aem_sling_model_generation_task()],
            callback=task_delay_callback  # Add delay after task
        )

    @task
    def aem_frontend_scss_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_frontend_scss_generation_task'], # type: ignore[index]
            output_file='output-aem_alchemist/05_scss.txt',
            context=[self.design_analysis_task(), self.aem_dialog_generation_task()],
            callback=task_delay_callback  # Add delay after task
        )

    @task
    def aem_frontend_js_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_frontend_js_generation_task'], # type: ignore[index]
            output_file='output-aem_alchemist/06_javascript.txt',
            context=[self.design_analysis_task(), self.aem_frontend_scss_generation_task()],
            callback=task_delay_callback  # Add delay after task
        )

    @task
    def aem_component_verification_task(self) -> Task:
        return Task(
            config=self.tasks_config['aem_component_verification_task'], # type: ignore[index]
            output_file='output-aem_alchemist/07_verification_report.txt',
            context=[self.design_analysis_task(), self.aem_frontend_js_generation_task()]
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

        # JSON-DRIVEN AEM WORKFLOW: Multi-Task Breakdown
        # Visual Strategist (JSON) → AEM Alchemist (6 separate file generation tasks + verification)
        # Following MOHH Project Structure: 6 Files Per Component
        return Crew(
            agents=[
                self.visual_strategist(),
                self.aem_alchemist()
            ],
            tasks=[
                # Phase 1: Design analysis - Generate JSON
                self.design_analysis_task(),

                # Phase 2: AEM component generation (6 files following MOHH standard)
                self.aem_component_definition_task(),    # 1/6: .content.xml (ui.apps)
                self.aem_htl_generation_task(),          # 2/6: HTL template (ui.apps)
                self.aem_sling_model_generation_task(),  # 3/6: Java Sling Model (core)
                self.aem_dialog_generation_task(),       # 4/6: Dialog XML (ui.apps)
                self.aem_frontend_scss_generation_task(), # 5/6: SCSS (ui.frontend)
                self.aem_frontend_js_generation_task(),  # 6/6: JavaScript (ui.frontend)

                # Phase 3: Verification - Confirm all files created
                self.aem_component_verification_task(),  # 7: Verify 6 files exist

                # Phase 4: Build and deploy (optional)
                # self.aem_build_deploy_task(),
                # self.aem_testing_task()
            ],
            process=Process.sequential,
            verbose=True,
        )

    
