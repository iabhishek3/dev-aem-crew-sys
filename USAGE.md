# How to Use the CrewAI + AEM Workflow

## Overview
This project has **two separate workflows**:

1. **HTML Creation Workflow** - Creates HTML components from design mockups
2. **AEM Conversion Workflow** - Converts HTML components to AEM components (interactive, one-at-a-time)

---

## Workflow 1: Create HTML Components

### Purpose
Analyzes design mockups and generates pixel-perfect HTML/CSS components.

### Command
```bash
crewai run
```

### What it does:
1. Analyzes the design image
2. Lists all components needed
3. Creates HTML files in `output/` folder

### Output:
```
output/
  ├── navbar.html
  ├── hero.html
  ├── button.html
  └── footer.html
```

---

## Workflow 2: Convert HTML to AEM Components (NEW!)

### Purpose
Converts HTML components to fully editable AEM components, one at a time, with user interaction.

### Command
```bash
run_aem
```

### What it does:

#### Step 1: Lists Components
```
Found the following HTML components:
1. navbar.html
2. hero.html
3. button.html
4. footer.html

Which component should I convert to AEM?
```

#### Step 2: User Selects Component
You select which component to work on (e.g., "navbar")

#### Step 3: Converts to AEM
Agent creates:
- HTL template
- Sling Model (Java)
- Component dialog
- ClientLib (CSS/JS)
- Component definition

#### Step 4: Builds & Deploys
```
Running Maven build...
BUILD SUCCESS
Deployed to: http://localhost:4502
```

#### Step 5: Testing
```
Please test the navbar component:

1. Open: http://localhost:4502/editor.html/content/hackaempoc/us/en.html
2. Add navbar component to page
3. Test the dialog - edit all fields
4. Verify component renders correctly

Did the component work correctly?
[ ] Yes, it works perfectly
[ ] No, there are issues
[ ] Partially works, needs fixes
```

#### Step 6: User Feedback
- **If "Yes"**: Component marked complete, returns to Step 1 for next component
- **If "No"**: Agent asks for details, fixes issues, rebuilds
- **If "Partial"**: Agent gathers specific issues and applies fixes

---

## Complete End-to-End Example

### 1. Create HTML Components
```bash
# Make sure you have design.png in the project root
crewai run
```

Wait for completion. HTML components will be in `output/` folder.

### 2. Convert to AEM (Interactive)
```bash
run_aem
```

Follow the interactive prompts:
- Select component to convert
- Wait for build
- Test in AEM
- Provide feedback
- Repeat for next component

---

## Configuration

### Update AEM Project Path
Edit `src/dev_aem_crew_sys/main.py` in the `run_aem()` function:

```python
inputs = {
    'output_folder': './output',
    'aem_project_path': r'C:\Dev\AEM-projects\dev-aem-crew\hackaempoc',  # Change this
    'aem_app_id': 'hackaempoc',                                          # Change this
    'aem_component_group': 'Hack AEM POC',                              # Change this
    'aem_namespace': 'hack/aem/poc'                                      # Change this
}
```

---

## Troubleshooting

### Error: "Template variable 'selected_component' not found"
**Solution:** You're trying to run both workflows at once. Use:
- `crewai run` for HTML creation only
- `run_aem` for AEM conversion only

### Error: "BUILD FAILED"
**Solution:** Check:
- AEM is running at http://localhost:4502
- Java compilation errors in Maven output
- Sling Model syntax

### Component doesn't appear in AEM
**Solution:**
- Check Package Manager: http://localhost:4502/crx/packmgr/index.jsp
- Verify component group matches allowed components
- Check CRXDE: http://localhost:4502/crx/de/index.jsp

---

## Key Features

### Interactive Selection
✅ You choose which component to convert
✅ One component at a time
✅ Full control over the workflow

### Complete AEM Components
✅ HTL template with proper syntax
✅ Sling Model with all properties
✅ Dialog with all editable fields
✅ ClientLib properly configured
✅ Everything author-friendly

### User Testing & Feedback
✅ Test each component before proceeding
✅ Provide feedback for fixes
✅ Iterative improvement
✅ Confirm component works before moving on

---

## Tips

1. **Always run HTML creation first** (`crewai run`) before AEM conversion (`run_aem`)

2. **Test thoroughly** - The agent waits for your confirmation before proceeding

3. **Provide clear feedback** - If something doesn't work, describe the issue clearly

4. **One at a time** - Don't try to convert all components at once. The workflow is designed to ensure quality by doing one component at a time.

5. **Check AEM logs** - If something fails, check AEM error logs for details

---

## Project Structure

```
dev_aem_crew_sys/
├── output/                    # HTML components (created by crewai run)
│   ├── navbar.html
│   ├── hero.html
│   └── button.html
├── src/
│   └── dev_aem_crew_sys/
│       ├── config/
│       │   ├── agents.yaml    # Agent definitions
│       │   └── tasks.yaml     # Task definitions
│       ├── tools/
│       │   ├── aem_file_writer_tool.py
│       │   └── maven_tool.py
│       ├── crew.py            # Crew configurations
│       └── main.py            # Entry points
└── design.png                 # Your design mockup

hackaempoc/                    # AEM project
├── core/                      # Java code (Sling Models)
├── ui.apps/                   # Components, dialogs, clientlibs
└── ui.content/                # Sample content
```

---

## Questions?

- Check `AEM_AGENT_SETUP.md` for detailed architecture
- Review the task descriptions in `src/dev_aem_crew_sys/config/tasks.yaml`
- Look at agent configurations in `src/dev_aem_crew_sys/config/agents.yaml`
