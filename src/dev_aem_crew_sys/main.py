#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

# CRITICAL: Apply Rich library fix BEFORE importing CrewAI
from dev_aem_crew_sys.fix_rich import apply_patch
apply_patch()

from dev_aem_crew_sys.crew import DevAemCrewSys

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew to create AEM components directly in your AEM project.

    IMPORTANT: Update the paths below before running:
    - design_path: Path to your design image (PNG/JPG)
    - aem_project_path: ABSOLUTE path to your AEM project root folder
    - aem_app_id: Your AEM application ID (used in component paths)
    - aem_namespace: Your Java package namespace (e.g., 'company/project' → 'company.project')
    - aem_component_group: Component group name for AEM authoring UI

    Example AEM Project Structure:
    /Users/dev/my-aem-project/          ← aem_project_path
    ├── core/
    │   └── src/main/java/com/mycompany/myapp/core/models/  ← Sling Models go here
    └── ui.apps/
        └── src/main/content/jcr_root/apps/myapp/components/ ← AEM components go here
    """
    inputs = {
        # Design image path (relative or absolute)
        'design_path': './table.png',

        # Output folder for logs (visual_strategist, ui_architect, aem_alchemist)
        'output_folder': './output',

        # AEM PROJECT CONFIGURATION - MOHH Websites Project
        # Absolute path to your AEM project root (where pom.xml is located)
        'aem_project_path': '/Users/abhishekkumar/Temus-space/aem-projects/mohh-websites-revamp',

        # Your AEM app ID (found in ui.apps/src/main/content/jcr_root/apps/)
        'aem_app_id': 'mohhwebsites',

        # Component group visible in AEM authoring UI (follows existing convention)
        'aem_component_group': 'MOHH Websites - Content',

        # Java package namespace (from archetype.properties: package=com.mohhwebsites)
        # Just use 'mohhwebsites' - system will convert to 'com.mohhwebsites'
        'aem_namespace': 'mohhwebsites',

        # Component selection (leave empty - agent will use design analysis)
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


def run_aem_only():
    """
    Run ONLY the AEM Alchemist agent (skips Visual Strategist).

    Use this for testing when you already have design_analysis.json from a previous run.
    This will skip the design analysis phase and directly generate AEM component files.

    PREREQUISITES:
    - output-visual_strategist/design_analysis.json must exist
    - Update the AEM project configuration below

    This runs all 7 AEM tasks:
    1. Component Definition (.content.xml)
    2. HTL Template (.html)
    3. Sling Model (.java)
    4. Dialog (_cq_dialog/.content.xml)
    5. SCSS (_component.scss)
    6. JavaScript (_component.js)
    7. Verification Report
    """
    import os

    # Check if design_analysis.json exists
    if not os.path.exists('output-visual_strategist/design_analysis.json'):
        print("❌ ERROR: design_analysis.json not found!")
        print("   Please run the full crew first with: run_crew run")
        print("   Or ensure output-visual_strategist/design_analysis.json exists")
        return

    print("✓ Found design_analysis.json")
    print("🚀 Starting AEM Alchemist (skipping Visual Strategist)...\n")

    inputs = {
        # Design image path (not used but required for task interpolation)
        'design_path': './table.png',

        # Output folder for logs
        'output_folder': './output',

        # AEM PROJECT CONFIGURATION - MOHH Websites Project
        'aem_project_path': '/Users/abhishekkumar/Temus-space/aem-projects/mohh-websites-revamp',
        'aem_app_id': 'mohhwebsites',
        'aem_component_group': 'MOHH Websites - Content',
        'aem_namespace': 'mohhwebsites',

        # Component selection (leave empty - agent will use design analysis)
        'selected_component': '',
        'component_name': ''
    }

    try:
        # Use the aem_only_crew instead of the full crew
        DevAemCrewSys().aem_only_crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the AEM-only crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'design_path': './first.png'
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
        'design_path': './first.png'
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
        "design_path": "./first.png"
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
