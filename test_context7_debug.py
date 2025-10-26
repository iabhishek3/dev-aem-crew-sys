#!/usr/bin/env python3
"""
Debug script to inspect Context7 MCP server tools and their schemas.
"""

import asyncio
import sys
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json


async def inspect_context7():
    """Connect to Context7 and inspect available tools"""

    # Windows-specific: Set ProactorEventLoop for better subprocess support
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    exit_stack = AsyncExitStack()

    try:
        print("Connecting to Context7 MCP server...")

        # Set up the Context7 MCP server parameters
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@upstash/context7-mcp"],
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

            # Initialize the session
            print("Initializing session...")
            await asyncio.wait_for(session.initialize(), timeout=30.0)
            print("Session initialized!\n")

            # List available tools
            print("Listing available tools...\n")
            tools_response = await asyncio.wait_for(
                session.list_tools(),
                timeout=10.0
            )

            if not tools_response.tools:
                print("No tools available from Context7 MCP server")
                return

            # Print each tool with its schema
            print(f"Found {len(tools_response.tools)} tool(s):\n")
            print("=" * 80)

            for idx, tool in enumerate(tools_response.tools, 1):
                print(f"\nTool #{idx}:")
                print(f"  Name: {tool.name}")
                print(f"  Description: {tool.description}")
                print(f"\n  Input Schema:")
                # Pretty print the input schema
                print(json.dumps(tool.inputSchema, indent=4))
                print("\n" + "-" * 80)

    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
    finally:
        await exit_stack.aclose()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(inspect_context7())
    finally:
        loop.close()
