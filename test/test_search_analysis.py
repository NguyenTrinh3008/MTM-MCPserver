"""
TEST KNOWLEDGE GRAPH SEARCH ANALYSIS
======================================

Tests server_http.py (auto-generated from FastAPI)
Detailed analysis of search results from FastMCP Knowledge Graph
"""

import asyncio
import json
from datetime import datetime
from fastmcp import Client

BASE_URL = "http://localhost:8002/mcp"  # server_http.py runs on port 8002
PROJECT_ID = "fastmcp_comprehensive_test"


async def analyze_search_quality():
    """Analyze search results quality from knowledge graph"""
    
    print("="*80)
    print("KNOWLEDGE GRAPH SEARCH ANALYSIS")
    print("="*80)
    print(f"Project ID: {PROJECT_ID}")
    print(f"Server URL: {BASE_URL}\n")
    
    async with Client(BASE_URL) as client:
        
        # Test queries based on ingested data
        test_queries = [
            {
                "query": "async await refactoring",
                "description": "Search for async/await patterns",
                "expected_context": "database functions, asyncpg, connection pooling"
            },
            {
                "query": "null pointer error fix",
                "description": "Search for defensive programming",
                "expected_context": "customer_email, NoneType, payment processing"
            },
            {
                "query": "bulk user update API",
                "description": "Search for API implementation",
                "expected_context": "rate limiting, validation, security"
            },
            {
                "query": "performance optimization N+1 queries",
                "description": "Search for performance patterns",
                "expected_context": "select_related, prefetch_related, caching"
            },
            {
                "query": "Redis caching strategy",
                "description": "Search for caching implementation",
                "expected_context": "TTL, cache invalidation, dashboard"
            }
        ]
        
        all_results = []
        
        for idx, test_case in enumerate(test_queries, 1):
            print(f"\n{'='*80}")
            print(f"QUERY {idx}: {test_case['description']}")
            print(f"{'='*80}")
            print(f"Search Query: '{test_case['query']}'")
            print(f"Expected Context: {test_case['expected_context']}")
            print()
            
            # Test each reranking strategy
            strategies = ["rrf", "mmr", "cross_encoder"]
            strategy_results = {}
            
            for strategy in strategies:
                print(f"\n--- Strategy: {strategy.upper()} ---")
                
                try:
                    result = await client.call_tool("search", {
                        "query": test_case["query"],
                        "group_id": PROJECT_ID,  # Correct parameter name
                        "limit": 5,
                        "rerank_strategy": strategy
                    })
                    
                    # Extract text content
                    if result.content and len(result.content) > 0:
                        content_text = result.content[0].text
                        
                        # Parse and display results
                        print(f"\nRaw Response Length: {len(content_text)} characters")
                        
                        # Try to extract structured information
                        if "[OK]" in content_text:
                            print("Status: [OK] Search successful")
                        
                        # Display preview (handle Unicode for Windows)
                        preview = content_text[:500] if len(content_text) > 500 else content_text
                        print(f"\nResponse Preview:")
                        print("-" * 80)
                        try:
                            print(preview)
                        except UnicodeEncodeError:
                            # Fallback for Windows console
                            print(preview.encode('ascii', 'replace').decode('ascii'))
                        if len(content_text) > 500:
                            print(f"\n... (truncated, {len(content_text) - 500} more characters)")
                        print("-" * 80)
                        
                        strategy_results[strategy] = {
                            "status": "success",
                            "response_length": len(content_text),
                            "content": content_text
                        }
                    else:
                        print("Status: [WARNING] Empty response")
                        strategy_results[strategy] = {
                            "status": "empty",
                            "response_length": 0,
                            "content": ""
                        }
                        
                except Exception as e:
                    print(f"Status: [ERROR] {str(e)}")
                    strategy_results[strategy] = {
                        "status": "error",
                        "error": str(e)
                    }
            
            # Compare strategies
            print(f"\n{'='*80}")
            print(f"STRATEGY COMPARISON FOR QUERY {idx}")
            print(f"{'='*80}")
            
            for strategy, result in strategy_results.items():
                status = result.get("status", "unknown")
                if status == "success":
                    length = result.get("response_length", 0)
                    print(f"{strategy.upper():15} - {status:10} - {length:5} chars")
                else:
                    print(f"{strategy.upper():15} - {status:10}")
            
            all_results.append({
                "query": test_case["query"],
                "description": test_case["description"],
                "expected_context": test_case["expected_context"],
                "results": strategy_results
            })
            
            await asyncio.sleep(1)
        
        # Overall Summary
        print(f"\n\n{'='*80}")
        print("OVERALL SEARCH QUALITY SUMMARY")
        print(f"{'='*80}\n")
        
        total_searches = len(test_queries) * len(strategies)
        successful_searches = sum(
            1 for r in all_results 
            for strategy_result in r["results"].values() 
            if strategy_result.get("status") == "success"
        )
        
        print(f"Total Search Operations: {total_searches}")
        print(f"Successful: {successful_searches}")
        print(f"Success Rate: {(successful_searches/total_searches*100):.1f}%\n")
        
        # Strategy performance
        print("Strategy Performance:")
        strategy_stats = {s: {"success": 0, "total": 0} for s in strategies}
        
        for result in all_results:
            for strategy, strategy_result in result["results"].items():
                strategy_stats[strategy]["total"] += 1
                if strategy_result.get("status") == "success":
                    strategy_stats[strategy]["success"] += 1
        
        for strategy, stats in strategy_stats.items():
            success_rate = (stats["success"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"  {strategy.upper():15} - {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        # Save detailed results
        output_file = "search_analysis_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.utcnow().isoformat(),
                "project_id": PROJECT_ID,
                "total_queries": len(test_queries),
                "total_searches": total_searches,
                "successful_searches": successful_searches,
                "success_rate": f"{(successful_searches/total_searches*100):.1f}%",
                "strategy_stats": {
                    strategy: {
                        "success": stats["success"],
                        "total": stats["total"],
                        "success_rate": f"{(stats['success']/stats['total']*100):.1f}%"
                    }
                    for strategy, stats in strategy_stats.items()
                },
                "detailed_results": all_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\nDetailed results saved to: {output_file}")
        
        return all_results


if __name__ == "__main__":
    results = asyncio.run(analyze_search_quality())
    print("\n[ANALYSIS COMPLETE]")

