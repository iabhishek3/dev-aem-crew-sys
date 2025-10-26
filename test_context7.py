#!/usr/bin/env python3
"""
Test script for Context7 MCP tool integration.
This tests the Context7Tool directly without running the full crew.
"""

from src.dev_aem_crew_sys.tools.context7_tool import Context7Tool

def test_context7():
    """Test Context7Tool with sample queries"""
    print("Testing Context7 MCP Tool Integration")
    print("=" * 80)

    # Create an instance of the Context7Tool
    context7 = Context7Tool()

    # Test 1: React (likely to be in Context7)
    print("\nTest 1: React Documentation")
    print("-" * 80)
    test_query_1 = "useState hook"
    print(f"Query: {test_query_1}")
    print(f"Library: react\n")

    result1 = context7._run(query=test_query_1, library="react")
    print("Result saved to: test_result_react.txt")
    with open("test_result_react.txt", "w", encoding="utf-8") as f:
        f.write(result1)
    print("\n" + "=" * 80)

    # Test 2: Try AEM
    print("\nTest 2: AEM Documentation")
    print("-" * 80)
    test_query_2 = "HTL data-sly-use syntax"
    print(f"Query: {test_query_2}")
    print(f"Library: aem\n")

    result2 = context7._run(query=test_query_2, library="aem")
    print("Result saved to: test_result_aem.txt")
    with open("test_result_aem.txt", "w", encoding="utf-8") as f:
        f.write(result2)
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_context7()
