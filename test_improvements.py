#!/usr/bin/env python3
"""
Test script to verify all improvements are working correctly.
"""
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_knowledge_base():
    """Test that knowledge base files are accessible"""
    import pathlib

    print("Testing Knowledge Base...")
    print("-" * 80)

    knowledge_dir = pathlib.Path("knowledge")
    required_files = [
        "aem_component_patterns.md",
        "htl_reference.md",
        "aem_validation_checklist.md"
    ]

    for filename in required_files:
        filepath = knowledge_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"✓ {filename} ({size:,} bytes)")
        else:
            print(f"✗ {filename} - MISSING!")

    print()


def test_htl_validator():
    """Test HTL validator tool"""
    print("Testing HTL Validator Tool...")
    print("-" * 80)

    from src.dev_aem_crew_sys.tools.htl_validator_tool import HTLValidatorTool

    validator = HTLValidatorTool()

    # Test with good HTL
    good_htl = '''
    <div data-sly-use.model="com.example.Model">
        <h2>${model.title}</h2>
        <img src="${model.image @ context='uri'}" alt="${model.imageAlt}">
        <a href="${model.link @ context='uri'}">${model.linkText}</a>
    </div>
    '''

    result = validator._run(htl_content=good_htl)
    if "PASS" in result or "No critical issues" in result:
        print("✓ HTL Validator works - Good HTL passed")
    else:
        print("! HTL Validator found issues in good HTL (might be suggestions)")

    # Test with bad HTL (missing contexts)
    bad_htl = '''
    <div>
        <a href="${properties.link}">${properties.text}</a>
        <script>var data = ${properties.data};</script>
    </div>
    '''

    result = validator._run(htl_content=bad_htl)
    if "SECURITY RISK" in result or "FAIL" in result:
        print("✓ HTL Validator works - Bad HTL detected")
    else:
        print("✗ HTL Validator did not catch security issues")

    print()


def test_context7():
    """Test Context7 tool"""
    print("Testing Context7 MCP Integration...")
    print("-" * 80)

    from src.dev_aem_crew_sys.tools.context7_tool import Context7Tool

    context7 = Context7Tool()

    print("Querying Context7 for React documentation...")
    result = context7._run(query="useState hook", library="react")

    if "DOCUMENTATION SEARCH RESULTS" in result:
        print("✓ Context7 works - Retrieved documentation")
        # Save result to file to avoid encoding issues
        with open("context7_test_result.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("  Result saved to: context7_test_result.txt")
    elif "Error" in result:
        print(f"✗ Context7 error: {result[:200]}...")
    else:
        print("? Context7 returned unexpected result")

    print()


def test_crew_integration():
    """Test that crew can be instantiated with improvements"""
    print("Testing Crew Integration...")
    print("-" * 80)

    try:
        from src.dev_aem_crew_sys.crew import DevAemCrewSys

        crew_instance = DevAemCrewSys()
        crew = crew_instance.crew()

        # Check agents
        agents = crew.agents
        print(f"✓ Crew created with {len(agents)} agents")

        # Check AEM Alchemist has new tools
        aem_agent = agents[2]  # Third agent is AEM Alchemist
        tools = aem_agent.tools
        tool_names = [tool.name for tool in tools]

        if "Context7 Documentation Search" in tool_names:
            print("✓ AEM Alchemist has Context7 tool")
        else:
            print("✗ AEM Alchemist missing Context7 tool")

        if "HTL Validator" in tool_names:
            print("✓ AEM Alchemist has HTL Validator tool")
        else:
            print("✗ AEM Alchemist missing HTL Validator tool")

        # Check knowledge sources
        if hasattr(crew, 'knowledge_sources') and crew.knowledge_sources:
            print(f"✓ Crew has {len(crew.knowledge_sources)} knowledge source(s)")
        else:
            print("! Crew has no knowledge sources (may be OK if files not found)")

    except Exception as e:
        print(f"✗ Error creating crew: {e}")

    print()


def main():
    print("\n" + "=" * 80)
    print("AEMplify Improvements Test Suite")
    print("=" * 80 + "\n")

    try:
        test_knowledge_base()
        test_htl_validator()
        test_context7()
        test_crew_integration()

        print("=" * 80)
        print("Testing Complete!")
        print("=" * 80)
        print("\nIf all tests passed, your improvements are working correctly!")
        print("Run your crew normally: uv run dev_aem_crew_sys")

    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
