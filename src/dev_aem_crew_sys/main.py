#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from dev_aem_crew_sys.crew import DevAemCrewSys

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew to create HTML components and convert them to AEM components.
    """
    inputs = {
        'design_path': './design.png',
        'output_folder': './output',
        'aem_project_path': r'C:\Dev\AEM-projects\dev-aem-crew\hackaempoc',
        'aem_app_id': 'hackaempoc',
        'aem_component_group': 'Hack AEM POC',
        'aem_namespace': 'hack/aem/poc',
        # Default selected component and component name are empty; the AEM agent will prompt the user
        'selected_component': '',
        'component_name': ''
    }

    # If output folder already contains HTML components, auto-fill selected_component
    try:
        import os
        out_dir = inputs.get('output_folder', './output')
        if os.path.isdir(out_dir):
            files = [f for f in os.listdir(out_dir) if f.lower().endswith('.html')]
            if files:
                # pick the first HTML file found
                inputs['selected_component'] = files[0]
                inputs['component_name'] = os.path.splitext(files[0])[0]
            else:
                # explicit placeholder to satisfy interpolation
                inputs['selected_component'] = ''
                inputs['component_name'] = 'component'
        else:
            inputs['selected_component'] = ''
            inputs['component_name'] = 'component'
    except Exception:
        inputs['selected_component'] = ''
        inputs['component_name'] = 'component'

    try:
        DevAemCrewSys().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

# Removed run_aem as it's now integrated into the main run function


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'design_path': './design.png'
    }
    try:
        DevAemCrewSys().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DevAemCrewSys().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'design_path': './design.png'
    }

    try:
        DevAemCrewSys().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "design_path": "./design.png"
    }

    # Provide defaults so task templates that reference these variables don't fail
    inputs.setdefault('output_folder', './output')
    inputs.setdefault('aem_project_path', r'C:\Dev\AEM-projects\dev-aem-crew\hackaempoc')
    inputs.setdefault('aem_app_id', 'hackaempoc')
    inputs.setdefault('aem_component_group', 'Hack AEM POC')
    inputs.setdefault('aem_namespace', 'hack/aem/poc')
    inputs.setdefault('selected_component', '')
    inputs.setdefault('component_name', '')

    try:
        result = DevAemCrewSys().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
