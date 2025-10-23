from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import subprocess
import os


class MavenToolInput(BaseModel):
    """Input schema for MavenTool."""
    aem_project_path: str = Field(..., description="The absolute path to the AEM project root")
    maven_command: str = Field(
        default="clean install -PautoInstallPackage",
        description="The Maven command to execute (default: 'clean install -PautoInstallPackage')"
    )


class MavenTool(BaseTool):
    name: str = "Maven Build Tool"
    description: str = (
        "Executes Maven commands in the AEM project directory. "
        "Use this to build and deploy AEM components. "
        "Provide the AEM project path and optionally the Maven command. "
        "Default command is 'clean install -PautoInstallPackage' which builds and deploys to local AEM."
    )
    args_schema: Type[BaseModel] = MavenToolInput

    def _run(self, aem_project_path: str, maven_command: str = "clean install -PautoInstallPackage") -> str:
        """
        Execute Maven build command in the AEM project directory.
        Returns build output and status.
        """
        try:
            # Verify the project path exists
            if not os.path.exists(aem_project_path):
                return f"Error: AEM project path does not exist: {aem_project_path}"

            # Verify pom.xml exists
            pom_path = os.path.join(aem_project_path, "pom.xml")
            if not os.path.exists(pom_path):
                return f"Error: pom.xml not found at: {pom_path}"

            # Prepare the Maven command
            full_command = f"mvn {maven_command}"

            print(f"Executing Maven build in: {aem_project_path}")
            print(f"Command: {full_command}")

            # Execute the Maven command
            process = subprocess.Popen(
                full_command,
                shell=True,
                cwd=aem_project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Get the output
            stdout, stderr = process.communicate()

            # Check if build was successful
            if process.returncode == 0:
                # Extract relevant information from output
                success_msg = "BUILD SUCCESS" if "BUILD SUCCESS" in stdout else ""

                result = f"""
Maven Build Completed Successfully!

{success_msg}

Project: {aem_project_path}
Command: {full_command}

Deployment Status: SUCCESS
Packages should now be installed in AEM at http://localhost:4502

To verify:
1. Check Package Manager: http://localhost:4502/crx/packmgr/index.jsp
2. Check CRXDE: http://localhost:4502/crx/de/index.jsp
3. Check AEM logs for any deployment issues

Last 20 lines of build output:
{chr(10).join(stdout.splitlines()[-20:])}
"""
                return result.strip()
            else:
                # Build failed - return error details
                result = f"""
Maven Build FAILED!

Project: {aem_project_path}
Command: {full_command}
Return Code: {process.returncode}

Error Output:
{stderr}

Last 30 lines of build output:
{chr(10).join(stdout.splitlines()[-30:])}

Common Issues:
- Java compilation errors: Check Sling Model syntax
- Missing dependencies: Check pom.xml
- AEM not running: Ensure AEM is running at http://localhost:4502
- Port conflicts: Check if port 4502 is available
"""
                return result.strip()

        except Exception as e:
            return f"Error executing Maven build: {str(e)}"
