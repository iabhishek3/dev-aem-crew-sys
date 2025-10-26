from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import asyncio
import os
import sys
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class Context7ToolInput(BaseModel):
    """Input schema for Context7Tool."""
    query: str = Field(..., description="The documentation query to search for (e.g., 'AEM HTL syntax', 'Sling Models', 'AEM components')")
    library: str = Field(default="aem", description="The library/framework to search docs for (e.g., 'aem', 'react', 'vue')")


class Context7Tool(BaseTool):
    name: str = "Context7 Documentation Search"
    description: str = (
        "Searches up-to-date documentation for AEM and other libraries using Context7 MCP server. "
        "This tool provides access to the latest API documentation, code examples, and best practices. "
        "Use this when you need accurate, current information about AEM components, HTL syntax, "
        "Sling Models, or any other technical documentation. Provide a query describing what you need "
        "to know (e.g., 'How to create AEM dialog', 'HTL data-sly-use syntax', 'Sling Model annotations')."
    )
    args_schema: Type[BaseModel] = Context7ToolInput

    def _run(self, query: str, library: str = "aem") -> str:
        """
        Search documentation using Context7 MCP server.
        Uses subprocess to connect to the Context7 MCP server via stdio.
        """
        try:
            # Windows-specific: Set ProactorEventLoop for better subprocess support
            if sys.platform == 'win32':
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

            # Run the async function synchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(self._search_docs(query, library))
                return result
            finally:
                loop.close()
        except Exception as e:
            return f"Error searching documentation: {str(e)}"

    async def _search_docs(self, query: str, library: str) -> str:
        """
        Async method to connect to Context7 MCP server and search documentation.
        """
        exit_stack = AsyncExitStack()

        try:
            # Get Context7 API key from environment (optional, but provides higher rate limits)
            api_key = os.getenv("CONTEXT7_API_KEY", "")

            # Set up the Context7 MCP server parameters
            # The server runs as an NPX command
            server_params = StdioServerParameters(
                command="npx",
                args=["-y", "@upstash/context7-mcp"] + (["--api-key", api_key] if api_key else []),
                env=None
            )

            # Connect to the MCP server using AsyncExitStack
            async with exit_stack:
                # Enter the stdio_client context
                stdio_transport = await exit_stack.enter_async_context(
                    stdio_client(server_params)
                )
                read, write = stdio_transport

                # Enter the ClientSession context
                session = await exit_stack.enter_async_context(
                    ClientSession(read, write)
                )

                # Initialize the session with timeout
                await asyncio.wait_for(session.initialize(), timeout=30.0)

                # List available tools from Context7
                tools_response = await asyncio.wait_for(
                    session.list_tools(),
                    timeout=10.0
                )

                if not tools_response.tools:
                    return "Error: No tools available from Context7 MCP server"

                # Context7 requires two-step process:
                # 1. resolve-library-id: Get the library ID from library name
                # 2. get-library-docs: Fetch docs using that library ID

                # Step 1: Resolve library ID
                resolve_result = await asyncio.wait_for(
                    session.call_tool(
                        "resolve-library-id",
                        arguments={"libraryName": library}
                    ),
                    timeout=30.0
                )

                # Extract library ID from the result
                library_id = None
                if resolve_result.content:
                    for content in resolve_result.content:
                        if hasattr(content, 'text'):
                            text = content.text
                            # Try to extract the library ID from the response
                            # Look for "Context7-compatible library ID: /path/to/library"
                            import re
                            # Match the pattern: "Context7-compatible library ID: " followed by the ID
                            id_match = re.search(r'Context7-compatible library ID:\s*(/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)?)', text)
                            if id_match:
                                library_id = id_match.group(1)
                                break
                            # Fallback: try to find any ID-like pattern if the above doesn't work
                            if not library_id:
                                id_match = re.search(r'(/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)', text)
                                if id_match:
                                    library_id = id_match.group(1)
                                    break

                if not library_id:
                    return f"Error: Could not resolve library ID for '{library}'. Context7 may not have documentation for this library. Try a different library name (e.g., 'react', 'vue', 'express')."

                # Step 2: Get library documentation with the query as topic
                result = await asyncio.wait_for(
                    session.call_tool(
                        "get-library-docs",
                        arguments={
                            "context7CompatibleLibraryID": library_id,
                            "topic": query,
                            "tokens": 5000  # Maximum tokens to retrieve
                        }
                    ),
                    timeout=60.0  # 60 second timeout for docs retrieval
                )

                # Extract and format the response
                if result.content:
                    response_text = ""
                    for content in result.content:
                        if hasattr(content, 'text'):
                            response_text += content.text + "\n"

                    if response_text:
                        return f"DOCUMENTATION SEARCH RESULTS\nLibrary: {library} (ID: {library_id})\nTopic: {query}\n\n{response_text}"
                    else:
                        return f"No documentation found for library '{library}' (ID: {library_id}) on topic: {query}"
                else:
                    return "No results returned from Context7"

        except FileNotFoundError:
            return (
                "Error: NPX/Node.js not found. Context7 requires Node.js to be installed.\n"
                "Please install Node.js from https://nodejs.org/ and try again."
            )
        except asyncio.TimeoutError:
            return "Error: Context7 MCP server request timed out. The server may be slow or unresponsive."
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return f"Error connecting to Context7 MCP server: {str(e)}\n\nDetails:\n{error_details}\n\nMake sure Node.js and NPX are installed and available in your PATH."
        finally:
            await exit_stack.aclose()
