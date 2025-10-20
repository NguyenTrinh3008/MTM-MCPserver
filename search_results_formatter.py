"""
SEARCH RESULTS FORMATTER FOR AGENT CONTEXT
==========================================

Convert search results from Knowledge Graph into human-readable prompts
for AI agents to use as context when answering user questions.

This module processes search results and formats them into structured
context that agents can use to provide informed responses about:
- Past coding solutions and patterns
- Bug fixes and their implementations  
- Performance optimizations
- API implementations and best practices
- Code refactoring examples
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class SearchResultsFormatter:
    """Format search results into agent-ready context prompts"""
    
    def __init__(self, results_file: str = "search_analysis_results.json"):
        """Initialize formatter with search results file"""
        self.results_file = results_file
        self.results_data = self._load_results()
    
    def _load_results(self) -> Dict[str, Any]:
        """Load search results from JSON file"""
        try:
            with open(self.results_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Results file {self.results_file} not found")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return {}
    
    def _clean_content(self, content: str) -> str:
        """Clean and normalize content text"""
        # Remove emoji and special characters
        content = re.sub(r'🔍|[^\x00-\x7F]+', '', content)
        
        # Clean up formatting
        content = re.sub(r'={80,}', '=' * 50, content)
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = content.strip()
        
        return content
    
    def _extract_knowledge_items(self, content: str) -> List[Dict[str, str]]:
        """Extract individual knowledge items from search content (JSON format)"""
        items = []
        
        try:
            # Parse JSON content
            data = json.loads(content)
            results = data.get("results", [])
            
            for result in results:
                # Extract key fields
                text = result.get("text", "")
                summary = result.get("summary", text)
                name = result.get("name", "Unknown")
                score = result.get("score", 0.0)
                
                # Optional metadata
                file_path = result.get("file_path", "")
                change_type = result.get("change_type", "")
                severity = result.get("severity", "")
                
                # Build item description
                relationship = name.replace("_", " ").title()
                
                # Build summary with metadata
                full_summary = summary
                if file_path:
                    full_summary += f" (File: {file_path})"
                if change_type:
                    full_summary += f" [Type: {change_type}]"
                if severity:
                    full_summary += f" [Severity: {severity}]"
                
                items.append({
                    "relationship": relationship,
                    "summary": full_summary,
                    "score": f"Score: {score:.3f}",
                    "raw_data": result  # Keep raw data for advanced processing
                })
        
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse JSON content: {e}")
            # Fallback: try old regex method for backward compatibility
            pass
        
        return items
    
    def format_query_context(self, query: str, strategy: str = "rrf") -> str:
        """Format search results for a specific query into agent context"""
        
        # Find the query in results
        query_data = None
        for result in self.results_data.get("detailed_results", []):
            if result["query"] == query:
                query_data = result
                break
        
        if not query_data:
            return f"No search results found for query: '{query}'"
        
        # Get results for the specified strategy
        strategy_result = query_data["results"].get(strategy, {})
        if strategy_result.get("status") != "success":
            return f"No successful results for query '{query}' with strategy '{strategy}'"
        
        content = strategy_result.get("content", "")
        cleaned_content = self._clean_content(content)
        knowledge_items = self._extract_knowledge_items(cleaned_content)
        
        # Format as agent context
        context = f"""KNOWLEDGE CONTEXT FOR: "{query}"
{'=' * 60}

SEARCH STRATEGY: {strategy.upper()}
EXPECTED CONTEXT: {query_data.get('expected_context', 'N/A')}

RELEVANT KNOWLEDGE FOUND:
"""
        
        for i, item in enumerate(knowledge_items, 1):
            context += f"""
{i}. RELATIONSHIP: {item['relationship']}
   KNOWLEDGE: {item['summary']}
   RELEVANCE: {item['score']}
"""
        
        if not knowledge_items:
            context += "\nNo structured knowledge items found in results."
        
        context += f"""
USAGE INSTRUCTIONS FOR AGENT:
- Use this knowledge to provide context-aware responses
- Reference specific relationships and patterns found
- Combine multiple knowledge items for comprehensive answers
- Mention that this information comes from past coding sessions
"""
        
        return context
    
    def format_all_queries_context(self, strategy: str = "rrf") -> str:
        """Format all search results into comprehensive agent context"""
        
        timestamp = self.results_data.get("timestamp", "unknown")
        project_id = self.results_data.get("project_id", "unknown")
        success_rate = self.results_data.get("success_rate", "unknown")
        
        context = f"""COMPREHENSIVE KNOWLEDGE CONTEXT
{'=' * 80}

PROJECT: {project_id}
ANALYSIS DATE: {timestamp}
SEARCH SUCCESS RATE: {success_rate}
STRATEGY: {strategy.upper()}

This context contains knowledge extracted from past coding conversations,
bug fixes, performance optimizations, and implementation patterns.

"""
        
        for i, result in enumerate(self.results_data.get("detailed_results", []), 1):
            query = result["query"]
            description = result["description"]
            expected_context = result["expected_context"]
            
            context += f"""
KNOWLEDGE DOMAIN {i}: {description.upper()}
{'-' * 60}
QUERY: "{query}"
EXPECTED TOPICS: {expected_context}

"""
            
            # Get strategy results
            strategy_result = result["results"].get(strategy, {})
            if strategy_result.get("status") == "success":
                content = strategy_result.get("content", "")
                cleaned_content = self._clean_content(content)
                knowledge_items = self._extract_knowledge_items(cleaned_content)
                
                for j, item in enumerate(knowledge_items, 1):
                    context += f"""  {i}.{j} {item['relationship']}
      → {item['summary']}
"""
                
                if not knowledge_items:
                    context += "  No structured knowledge found.\n"
            else:
                context += f"  Search failed: {strategy_result.get('status', 'unknown')}\n"
        
        context += f"""

AGENT USAGE GUIDELINES:
{'=' * 80}

1. CONTEXT INTEGRATION:
   - Use this knowledge to enhance responses about coding topics
   - Reference specific patterns and solutions from past sessions
   - Combine knowledge from multiple domains for comprehensive answers

2. RESPONSE PATTERNS:
   - "Based on past coding sessions, we've seen..."
   - "A similar pattern was used when..."
   - "Previous implementations show that..."
   - "From our knowledge base, the recommended approach is..."

3. KNOWLEDGE DOMAINS COVERED:
   - Async/await refactoring patterns
   - Null pointer error fixes and defensive programming
   - API implementation with security considerations
   - Performance optimization (N+1 queries, caching)
   - Redis caching strategies and best practices

4. CONFIDENCE LEVELS:
   - High confidence: Multiple knowledge items support the answer
   - Medium confidence: Some relevant patterns found
   - Low confidence: Limited or indirect knowledge available

5. WHEN TO USE:
   - User asks about coding patterns or best practices
   - User needs examples of past implementations
   - User wants to learn from previous solutions
   - User asks "how did we handle X before?"
"""
        
        return context
    
    def generate_example_prompts(self) -> List[Dict[str, str]]:
        """Generate example user questions and agent responses using the knowledge"""
        
        examples = []
        
        # Example 1: Async refactoring
        examples.append({
            "user_question": "How should I convert my synchronous database functions to async/await?",
            "agent_context": self.format_query_context("async await refactoring"),
            "sample_response": """Based on past coding sessions, here's the recommended approach for async/await conversion:

**From our knowledge base:**
- Convert `def` to `async def` for database functions
- Use `await` for all I/O operations (database calls, API requests)
- Switch to async libraries like `asyncpg` for PostgreSQL
- Update all callers to use `await` when calling the converted functions

**Implementation pattern we've used:**
```python
# Before: user = get_user_data(user_id)
# After:  user = await get_user_data(user_id)
```

This pattern has shown significant performance improvements in previous implementations, with response times improving from 450ms to 85ms (81% faster) and the ability to handle 10x concurrent requests."""
        })
        
        # Example 2: Null pointer fixes
        examples.append({
            "user_question": "I'm getting NoneType errors in my payment processing. How should I fix this?",
            "agent_context": self.format_query_context("null pointer error fix"),
            "sample_response": """Based on similar issues we've resolved before, this is typically a defensive programming problem:

**From past bug fixes:**
- The error occurs when `customer_email` can be None for guest checkouts
- Code assumes all payments have customer emails without checking
- Solution: Use defensive programming with proper null checks

**Recommended fix pattern:**
```python
# Before: theme = user_data['user_preferences']['theme']
# After:  
preferences = user_data.get('user_preferences', {})
theme = preferences.get('theme', 'default')
```

**Additional improvements from our knowledge base:**
- Add default value initialization for new users
- Include comprehensive test cases for null scenarios
- Add logging for None cases to track frequency"""
        })
        
        return examples
    
    def save_formatted_context(self, output_file: str = "agent_knowledge_context.txt"):
        """Save formatted context to file for agent use"""
        
        context = self.format_all_queries_context()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(context)
        
        print(f"Agent context saved to: {output_file}")
        return output_file
    
    def save_example_prompts(self, output_file: str = "agent_example_prompts.json"):
        """Save example prompts to JSON file"""
        
        examples = self.generate_example_prompts()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(examples, f, indent=2, ensure_ascii=False)
        
        print(f"Example prompts saved to: {output_file}")
        return output_file


def main():
    """Main function to demonstrate the formatter"""
    
    print("SEARCH RESULTS FORMATTER")
    print("=" * 80)
    
    # Initialize formatter
    formatter = SearchResultsFormatter("search_analysis_results.json")
    
    if not formatter.results_data:
        print("No search results data available")
        return
    
    print(f"Loaded results for project: {formatter.results_data.get('project_id')}")
    print(f"Total queries analyzed: {formatter.results_data.get('total_queries')}")
    print(f"Success rate: {formatter.results_data.get('success_rate')}")
    print()
    
    # Generate context for specific queries
    queries = [
        "async await refactoring",
        "null pointer error fix", 
        "bulk user update API",
        "performance optimization N+1 queries",
        "Redis caching strategy"
    ]
    
    print("INDIVIDUAL QUERY CONTEXTS:")
    print("-" * 80)
    
    for query in queries:
        print(f"\n[QUERY] {query}")
        context = formatter.format_query_context(query)
        print(context[:300] + "..." if len(context) > 300 else context)
    
    # Save comprehensive context
    print(f"\n{'=' * 80}")
    print("SAVING AGENT CONTEXT FILES...")
    print("=" * 80)
    
    context_file = formatter.save_formatted_context()
    examples_file = formatter.save_example_prompts()
    
    print(f"\nFiles created:")
    print(f"1. {context_file} - Complete knowledge context for agent")
    print(f"2. {examples_file} - Example user questions and responses")
    
    print(f"\nUSAGE:")
    print(f"- Load {context_file} as system context for your AI agent")
    print(f"- Use the knowledge to enhance responses about coding topics")
    print(f"- Reference past patterns and solutions in your answers")


if __name__ == "__main__":
    main()

