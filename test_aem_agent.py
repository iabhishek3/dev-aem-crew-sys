#!/usr/bin/env python
"""
Test script to run only the AEM agent tasks directly.
This allows testing the AEM conversion without running the full crew.
"""
import sys
import warnings
import os
from dotenv import load_dotenv
from dev_aem_crew_sys.crew import DevAemCrewSys
from crewai import Crew, Process

# Load environment variables
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run_aem_only():
    """
    Run only the AEM-related tasks (component selection, conversion, build, test).
    Assumes HTML components already exist in the output folder.
    """
    inputs = {
        'design_path': './design.png',
        'output_folder': './output',
        'aem_project_path': r'C:\Dev\AEM-projects\dev-aem-crew\hackaempoc',
        'aem_app_id': 'hackaempoc',
        'aem_component_group': 'Hack AEM POC',
        'aem_namespace': 'hack/aem/poc',
        'selected_component': 'navbar.html',
        'component_name': 'navbar'
    }

    print("=" * 80)
    print("Testing AEM Agent Only")
    print("=" * 80)
    print(f"Component to convert: {inputs['selected_component']}")
    print(f"Output folder: {inputs['output_folder']}")
    print(f"AEM project: {inputs['aem_project_path']}")
    print("=" * 80)
    print()

    try:
        # Create the crew instance
        crew_instance = DevAemCrewSys()

        # Get only the AEM agent
        aem_agent = crew_instance.aem_developer()

        # Get only the AEM tasks
        aem_tasks = [
            crew_instance.aem_component_list_task(),
            crew_instance.aem_component_conversion_task(),
            crew_instance.aem_build_deploy_task(),
            crew_instance.aem_testing_task()
        ]

        print(f"Created AEM agent with tools: {[tool.name for tool in aem_agent.tools]}")
        print(f"Running {len(aem_tasks)} AEM tasks...")
        print()

        # Create a mini crew with just the AEM agent and tasks
        aem_crew = Crew(
            agents=[aem_agent],
            tasks=aem_tasks,
            process=Process.sequential,
            verbose=True
        )

        # Run the AEM crew
        result = aem_crew.kickoff(inputs=inputs)

        print()
        print("=" * 80)
        print("AEM Agent Test Complete!")
        print("=" * 80)
        print(f"Result: {result}")

        return result

    except Exception as e:
        print()
        print("=" * 80)
        print("AEM Agent Test Failed")
        print("=" * 80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise Exception(f"An error occurred while testing the AEM agent: {e}")

if __name__ == "__main__":
    run_aem_only()
