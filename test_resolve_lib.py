#!/usr/bin/env python3
"""
Test script to see what resolve-library-id returns.
"""

import asyncio
import sys
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_resolve():
    """Test resolve-library-id"""

    # Windows-specific
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    exit_stack = AsyncExitStack()

    try:
        print("Connecting to Context7...")

        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@upstash/context7-mcp"],
            env=None
        )

        async with exit_stack:
            stdio_transport = await exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            read, write = stdio_transport

            session = await exit_stack.enter_async_context(
                ClientSession(read, write)
            )

            await asyncio.wait_for(session.initialize(), timeout=30.0)
            print("Connected!\n")

            # Test different library names
            test_libraries = ["react", "vue", "aem", "express", "next.js"]

            for lib_name in test_libraries:
                print(f"\n{'='*80}")
                print(f"Testing library: {lib_name}")
                print('='*80)

                resolve_result = await asyncio.wait_for(
                    session.call_tool(
                        "resolve-library-id",
                        arguments={"libraryName": lib_name}
                    ),
                    timeout=30.0
                )

                if resolve_result.content:
                    for content in resolve_result.content:
                        if hasattr(content, 'text'):
                            # Write to file to avoid console encoding issues
                            with open(f"resolve_{lib_name}.txt", "w", encoding="utf-8") as f:
                                f.write(content.text)
                            print(f"\nResponse saved to: resolve_{lib_name}.txt")

    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        traceback.print_exc()
    finally:
        await exit_stack.aclose()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(test_resolve())
    finally:
        loop.close()
