from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import re
import os


class HTLValidatorInput(BaseModel):
    """Input schema for HTLValidatorTool."""
    htl_content: str = Field(..., description="The HTL template content to validate")
    file_path: str = Field(default="", description="Optional file path to read HTL content from")


class HTLValidatorTool(BaseTool):
    name: str = "HTL Validator"
    description: str = (
        "Validates HTL (HTML Template Language) code for common issues, security vulnerabilities, "
        "and best practices. Checks for proper XSS protection contexts, correct syntax, "
        "AEM component patterns, and code quality. Returns a detailed report with issues, "
        "warnings, and suggestions for improvement."
    )
    args_schema: Type[BaseModel] = HTLValidatorInput

    def _run(self, htl_content: str = "", file_path: str = "") -> str:
        """
        Validate HTL template content for issues and best practices.
        """
        try:
            # If file_path provided, read from file
            if file_path and os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    htl_content = f.read()

            if not htl_content:
                return "Error: No HTL content provided to validate"

            issues = []
            warnings = []
            suggestions = []

            # Run validation checks
            self._check_xss_contexts(htl_content, issues, warnings)
            self._check_htl_syntax(htl_content, issues, warnings)
            self._check_best_practices(htl_content, warnings, suggestions)
            self._check_security(htl_content, issues, warnings)
            self._check_component_patterns(htl_content, suggestions)

            # Build validation report
            report = self._build_report(htl_content, issues, warnings, suggestions)

            return report

        except Exception as e:
            return f"Error validating HTL: {str(e)}"

    def _check_xss_contexts(self, content: str, issues: list, warnings: list):
        """Check for proper XSS context usage"""

        # Find all HTL expressions
        expressions = re.findall(r'\$\{([^}]+)\}', content)

        for expr in expressions:
            # Check if expression is in a potentially dangerous location

            # Expression without @ context in HTML content area
            if '@ context' not in expr and '@context' not in expr:
                # Check if it's in an attribute that might need context
                if re.search(r'href=.*?\$\{' + re.escape(expr) + r'\}', content):
                    warnings.append(
                        f"Expression '${{{expr}}}' used in href without @ context='uri'. "
                        f"Consider: href=\"${{{expr} @ context='uri'}}\""
                    )
                elif re.search(r'<script[^>]*>.*?\$\{' + re.escape(expr) + r'\}', content, re.DOTALL):
                    issues.append(
                        f"Expression '${{{expr}}}' used in <script> without @ context='scriptString'. "
                        f"SECURITY RISK: XSS vulnerability!"
                    )
                elif re.search(r'<style[^>]*>.*?\$\{' + re.escape(expr) + r'\}', content, re.DOTALL):
                    warnings.append(
                        f"Expression '${{{expr}}}' used in <style> without @ context='styleString'"
                    )

            # Check for context='unsafe' usage
            if "context='unsafe'" in expr or 'context="unsafe"' in expr:
                issues.append(
                    f"SECURITY RISK: context='unsafe' used in expression '${{{expr}}}'. "
                    f"This disables XSS protection. Use appropriate context instead."
                )

    def _check_htl_syntax(self, content: str, issues: list, warnings: list):
        """Check for common HTL syntax errors"""

        # Check for data-sly-use with incorrect format
        invalid_use = re.findall(r'data-sly-use="([^"]+)"', content)
        for use_expr in invalid_use:
            if not '=' in use_expr:
                warnings.append(
                    f"data-sly-use=\"{use_expr}\" might be missing object name. "
                    f"Should be: data-sly-use.objectName=\"{use_expr}\""
                )

        # Check for unbalanced HTL expressions
        open_braces = content.count('${')
        close_braces = content.count('}')
        if open_braces != close_braces:
            issues.append(
                f"Unbalanced HTL expressions: {open_braces} opening '${{' but {close_braces} closing '}}'"
            )

        # Check for data-sly-test without unwrap on non-semantic elements
        test_on_div = re.findall(r'<div[^>]*data-sly-test[^>]*>', content)
        for match in test_on_div:
            if 'data-sly-unwrap' not in match:
                warnings.append(
                    f"data-sly-test on <div> without data-sly-unwrap. "
                    f"Consider using <sly data-sly-test> instead for cleaner markup."
                )

    def _check_best_practices(self, content: str, warnings: list, suggestions: list):
        """Check for HTL best practices"""

        # Check for inline styles (should use CSS classes)
        if re.search(r'style="[^"]*\$\{', content):
            warnings.append(
                "Inline styles with dynamic values detected. "
                "Consider using CSS classes with data-sly-attribute.class instead."
            )

        # Check for hardcoded text that should be i18n
        hardcoded_text = re.findall(r'>[A-Z][a-z]{4,}[^<]*<', content)
        if len(hardcoded_text) > 3:
            suggestions.append(
                f"Found {len(hardcoded_text)} instances of hardcoded text. "
                f"Consider using i18n: ${{'key' @ i18n}}"
            )

        # Check for missing alt attributes on images
        imgs_without_alt = re.findall(r'<img(?![^>]*\balt=)[^>]*>', content)
        if imgs_without_alt:
            issues.append(
                f"Found {len(imgs_without_alt)} <img> tag(s) without alt attribute. "
                f"This is an accessibility issue (WCAG violation)."
            )

        # Check for data-sly-resource without resourceType
        resource_without_type = re.findall(
            r'data-sly-resource="[^"]*"(?![^>]*resourceType)',
            content
        )
        if resource_without_type:
            warnings.append(
                f"data-sly-resource used without explicit resourceType. "
                f"Consider specifying @ resourceType for better control."
            )

        # Check for empty href
        if 'href=""' in content or "href=''" in content:
            warnings.append(
                "Empty href attribute found. This can cause page reload. "
                "Use href=\"#\" or data-sly-attribute.href with conditional."
            )

    def _check_security(self, content: str, issues: list, warnings: list):
        """Check for security issues"""

        # Check for direct property access in href without uri context
        dangerous_hrefs = re.findall(r'href="\$\{properties\.([^}@]+)\}"', content)
        for prop in dangerous_hrefs:
            if '@ context' not in prop:
                issues.append(
                    f"SECURITY RISK: properties.{prop} used in href without @ context='uri'. "
                    f"This could allow JavaScript injection. "
                    f"Fix: href=\"${{properties.{prop} @ context='uri'}}\""
                )

        # Check for innerHTML-like patterns
        if re.search(r'@ context=[\'"]html[\'"]', content):
            warnings.append(
                "@ context='html' detected. Ensure the content source is trusted "
                "to prevent XSS attacks. Prefer text context when possible."
            )

        # Check for onclick or other event handlers with HTL expressions
        event_handlers = re.findall(r'on\w+="[^"]*\$\{[^}]+\}', content)
        if event_handlers:
            issues.append(
                f"SECURITY RISK: Found {len(event_handlers)} event handler(s) with HTL expressions. "
                f"This is dangerous and should be avoided. Use external JavaScript instead."
            )

    def _check_component_patterns(self, content: str, suggestions: list):
        """Check for common AEM component patterns"""

        # Check if data-sly-use is present (likely needs a model)
        if not re.search(r'data-sly-use\.\w+', content):
            suggestions.append(
                "No data-sly-use found. Consider using a Sling Model for complex logic "
                "instead of accessing properties directly."
            )

        # Check for list iteration without index/metadata usage
        list_iterations = re.findall(r'data-sly-list\.(\w+)=', content)
        for item_name in list_iterations:
            if f'{item_name}List' not in content:
                suggestions.append(
                    f"data-sly-list.{item_name} could use {item_name}List metadata "
                    f"for index, first, last, etc."
                )

        # Check for template definitions
        if 'data-sly-template' in content and 'data-sly-call' not in content:
            warnings.append(
                "Template defined but not called. Ensure templates are used with data-sly-call."
            )

    def _build_report(self, content: str, issues: list, warnings: list, suggestions: list) -> str:
        """Build validation report"""

        report_lines = ["HTL VALIDATION REPORT", "=" * 80, ""]

        # Summary
        total_issues = len(issues) + len(warnings)
        severity = "FAIL" if issues else ("WARNINGS" if warnings else "PASS")

        report_lines.append(f"Status: {severity}")
        report_lines.append(f"Lines of HTL: {len(content.splitlines())}")
        report_lines.append(f"Critical Issues: {len(issues)}")
        report_lines.append(f"Warnings: {len(warnings)}")
        report_lines.append(f"Suggestions: {len(suggestions)}")
        report_lines.append("")

        # Critical Issues
        if issues:
            report_lines.append("CRITICAL ISSUES (Must Fix):")
            report_lines.append("-" * 80)
            for i, issue in enumerate(issues, 1):
                report_lines.append(f"{i}. {issue}")
            report_lines.append("")

        # Warnings
        if warnings:
            report_lines.append("WARNINGS (Should Fix):")
            report_lines.append("-" * 80)
            for i, warning in enumerate(warnings, 1):
                report_lines.append(f"{i}. {warning}")
            report_lines.append("")

        # Suggestions
        if suggestions:
            report_lines.append("SUGGESTIONS (Consider):")
            report_lines.append("-" * 80)
            for i, suggestion in enumerate(suggestions, 1):
                report_lines.append(f"{i}. {suggestion}")
            report_lines.append("")

        # Final verdict
        report_lines.append("=" * 80)
        if not issues and not warnings:
            report_lines.append("✓ HTL code looks good! No critical issues or warnings found.")
        elif issues:
            report_lines.append("✗ HTL validation FAILED. Please fix critical issues before deployment.")
        else:
            report_lines.append("⚠ HTL validation passed with warnings. Review and address warnings.")

        return "\n".join(report_lines)
