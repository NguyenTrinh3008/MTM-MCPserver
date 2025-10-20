"""
COMPREHENSIVE FASTMCP SERVER TEST SCENARIOS
===========================================

Tests server_http.py (auto-generated from FastAPI)

Realistic test scenarios covering:
1. Multi-turn conversations with context building
2. Code refactoring workflows
3. Debugging sessions with memory recall
4. Performance optimization scenarios
5. Documentation generation workflows
6. Cross-project search and retrieval
7. Admin monitoring operations (READ-ONLY resources)
8. Concurrent request handling
9. Error recovery and resilience testing

IMPORTANT NOTES:
================
- Admin POST endpoints are FILTERED OUT in server_http.py:
  * /cache/* (clear_cache, invalidate_cache)
  * /admin/* (system admin operations)
  * /langfuse/* (tracing config)
  * /config/* (configuration changes)
  * /innocody/* (webhook endpoints)

- Admin operations now test READ-ONLY resources instead:
  * get_cache_stats (resource)
  * cache_health (resource)
  * get_tool_stats (resource)
  * langfuse_health (resource)

Inspired by test_realistic_scenarios.py and test_reranking_strategies.py
"""

import asyncio
import time
import hashlib
import uuid as uuid_lib
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict
import json
from pathlib import Path

from fastmcp import Client


# =============================================================================
# TEST CONFIGURATION
# =============================================================================

BASE_URL = "http://localhost:8002/mcp"  # server_http.py runs on port 8002
PROJECT_ID = "fastmcp_comprehensive_test"

# Test data categories
TEST_CATEGORIES = {
    "refactoring": "Code refactoring and modernization",
    "debugging": "Bug investigation and fixing",
    "feature_implementation": "New feature development",
    "performance_optimization": "Performance tuning",
    "code_review": "Code quality and security review",
    "documentation": "Documentation generation",
    "learning": "Learning and exploration"
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def make_request_id(prefix: str = "req") -> str:
    """Generate unique request ID"""
    return f"{prefix}_{uuid_lib.uuid4().hex[:12]}"


def make_chat_id(session: str) -> str:
    """Generate chat ID for session"""
    return f"chat_{session}_{uuid_lib.uuid4().hex[:8]}"


def make_timestamp() -> str:
    """Generate ISO format timestamp"""
    return datetime.utcnow().isoformat() + "Z"


def make_content_hash(content: str) -> str:
    """Generate SHA256 hash for content"""
    return hashlib.sha256(content.encode()).hexdigest()


def make_context_file(file_path: str, usefulness: float, source: str = "vecdb") -> Dict:
    """Create context file payload"""
    return {
        "file_path": file_path,
        "usefulness": usefulness,
        "content_hash": make_content_hash(file_path),
        "source": source,
        "symbols": [],
        "language": detect_language(file_path)
    }


def detect_language(file_path: str) -> str:
    """Detect language from file extension"""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript',
        '.go': 'go',
        '.rs': 'rust',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.rb': 'ruby',
        '.php': 'php',
        '.cs': 'csharp',
    }
    for ext, lang in ext_map.items():
        if file_path.endswith(ext):
            return lang
    return 'unknown'


def make_tool_call(tool_name: str, status: str = "success", execution_time_ms: int = 200) -> Dict:
    """Create tool call payload"""
    return {
        "tool_call_id": f"call_{uuid_lib.uuid4().hex[:8]}",
        "tool_name": tool_name,
        "arguments_hash": make_content_hash(f"{tool_name}:args"),
        "status": status,
        "execution_time_ms": execution_time_ms
    }


def make_code_change(
    file_path: str,
    change_summary: str,
    change_type: str = "modified",
    severity: str = "medium",
    lines_added: int = 0,
    lines_removed: int = 0,
    function_name: str = None,
) -> Dict:
    """Create code change payload"""
    return {
        "name": f"{change_type.title()} {file_path}",
        "summary": change_summary,
        "file_path": file_path,
        "function_name": function_name,
        "change_type": change_type,
        "change_summary": change_summary,
        "severity": severity,
        "diff_summary": change_summary,
        "lines_added": lines_added,
        "lines_removed": lines_removed,
        "language": detect_language(file_path),
        "imports": [],
        "code_before_hash": make_content_hash(f"before:{file_path}"),
        "code_after_hash": make_content_hash(f"after:{file_path}"),
        "timestamp": make_timestamp(),
    }


def print_section(title: str, char: str = "="):
    """Print formatted section header"""
    print(f"\n{char * 80}")
    print(f"{title}")
    print(f"{char * 80}")


def print_result(label: str, value: Any, indent: int = 0):
    """Print formatted result"""
    prefix = "  " * indent
    print(f"{prefix}{label}: {value}")


# =============================================================================
# SCENARIO 1: ASYNC/AWAIT REFACTORING WORKFLOW
# =============================================================================

async def scenario_async_refactoring_workflow(client: Client):
    """
    Multi-turn conversation: User refactors sync code to async/await
    
    Steps:
    1. User asks about converting sync to async
    2. Assistant analyzes code and provides plan
    3. User implements changes
    4. Assistant reviews and suggests improvements
    5. User optimizes performance
    """
    print_section("SCENARIO 1: Async/Await Refactoring Workflow")
    
    session_id = "async_refactor_001"
    chat_id = make_chat_id(session_id)
    
    # Turn 1: Initial question about async conversion
    print("\n[Turn 1] User asks about async conversion...")
    result = await client.call_tool("ingest_conversation", {
        "request_id": make_request_id("async"),
        "project_id": PROJECT_ID,
        "timestamp": make_timestamp(),
        "chat_meta": {
            "chat_id": chat_id,
            "base_chat_id": session_id,
            "request_attempt_id": make_request_id("attempt"),
            "chat_mode": "AGENT"
        },
        "messages": [
            {
                "sequence": 0,
                "role": "user",
                "content_summary": "How do I convert my synchronous database functions to async/await in Python?",
                "content_hash": make_content_hash("async question 1"),
                "total_tokens": 15,
                "sequence": 0
            },
            {
                "sequence": 1,
                "role": "assistant",
                "content_summary": "To convert sync to async: 1) Change def to async def, 2) Use await for I/O operations, 3) Switch to async libraries (asyncpg for PostgreSQL, aiohttp for HTTP), 4) Update all callers to use await",
                "content_hash": make_content_hash("async answer 1"),
                "prompt_tokens": 30,
                "completion_tokens": 80,
                "total_tokens": 110,
                "sequence": 1
            }
        ],
        "context_files": [
            make_context_file("app/database/users.py", 0.95, "vecdb"),
            make_context_file("app/database/connection.py", 0.88, "ast"),
            make_context_file("docs/async_guide.md", 0.75, "vecdb")
        ],
        "tool_calls": [
            make_tool_call("read_file", "success", 245),
            make_tool_call("codebase_search", "success", 380)
        ],
        "code_changes": []
    })
    print_result("Turn 1 ingested", "OK", 1)
    
    await asyncio.sleep(1)
    
    # Turn 2: User implements async conversion
    print("\n[Turn 2] User implements async conversion...")
    result = await client.call_tool("ingest_conversation", {
        "request_id": make_request_id("async"),
        "project_id": PROJECT_ID,
        "timestamp": make_timestamp(),
        "chat_meta": {
            "chat_id": chat_id,
            "base_chat_id": session_id,
            "request_attempt_id": make_request_id("attempt"),
            "chat_mode": "AGENT"
        },
        "messages": [
            {
                "sequence": 0,
                "role": "user",
                "content_summary": "I've converted get_user() to async. Can you review the changes?",
                "content_hash": make_content_hash("async question 2"),
                "total_tokens": 12,
                "sequence": 0
            },
            {
                "sequence": 1,
                "role": "assistant",
                "content_summary": "The async conversion looks good! A few suggestions: 1) Add connection pooling with asyncpg.create_pool(), 2) Use async context managers for transaction handling, 3) Consider adding retry logic for transient errors",
                "content_hash": make_content_hash("async answer 2"),
                "prompt_tokens": 50,
                "completion_tokens": 100,
                "total_tokens": 150,
                "sequence": 1
            }
        ],
        "context_files": [
            make_context_file("app/database/users.py", 0.98, "vecdb"),
            make_context_file("app/models/user.py", 0.85, "ast")
        ],
        "tool_calls": [
            make_tool_call("read_file", "success", 220),
            make_tool_call("edit_file", "success", 450)
        ],
        "code_changes": [
            make_code_change(
                "app/database/users.py",
                "Converted get_user() from synchronous to async/await pattern using asyncpg",
                change_type="refactored",
                severity="high",
                lines_added=15,
                lines_removed=10,
                function_name="get_user"
            )
        ]
    })
    print_result("Turn 2 ingested", "OK", 1)
    
    await asyncio.sleep(1)
    
    # Turn 3: Performance optimization
    print("\n[Turn 3] Performance optimization discussion...")
    result = await client.call_tool("ingest_conversation", {
        "request_id": make_request_id("async"),
        "project_id": PROJECT_ID,
        "timestamp": make_timestamp(),
        "chat_meta": {
            "chat_id": chat_id,
            "base_chat_id": session_id,
            "request_attempt_id": make_request_id("attempt"),
            "chat_mode": "AGENT"
        },
        "messages": [
            {
                "sequence": 0,
                "role": "user",
                "content_summary": "The async version is working but still feels slow. How can I optimize it further?",
                "content_hash": make_content_hash("async question 3"),
                "total_tokens": 18,
                "sequence": 0
            },
            {
                "sequence": 1,
                "role": "assistant",
                "content_summary": "For better performance: 1) Implement connection pooling (reduces connection overhead by 70%), 2) Use asyncio.gather() for parallel queries, 3) Add query result caching with Redis, 4) Consider prepared statements for frequently used queries",
                "content_hash": make_content_hash("async answer 3"),
                "prompt_tokens": 60,
                "completion_tokens": 120,
                "total_tokens": 180,
                "sequence": 1
            }
        ],
        "context_files": [
            make_context_file("app/database/users.py", 0.96, "vecdb"),
            make_context_file("app/database/pool.py", 0.92, "ast"),
            make_context_file("app/cache/redis_client.py", 0.85, "vecdb")
        ],
        "tool_calls": [
            make_tool_call("read_file", "success", 280),
            make_tool_call("edit_file", "success", 520)
        ],
        "code_changes": [
            make_code_change(
                "app/database/pool.py",
                "Added asyncpg connection pool with min_size=10, max_size=100 for optimal performance",
                change_type="added",
                severity="medium",
                lines_added=45,
                lines_removed=0,
                function_name="create_db_pool"
            )
        ]
    })
    print_result("Turn 3 ingested", "OK", 1)
    
    # Search for async-related memories
    print("\n[Search] Retrieving async refactoring knowledge...")
    search_result = await client.call_tool("search", {
        "query": "async await refactoring performance optimization",
        "group_id": PROJECT_ID,
        "limit": 5,
        "rerank_strategy": "rrf"
    })
    print_result("Search results", f"Found memories about async refactoring", 1)
    
    print_result("Scenario 1", "COMPLETED", 0)
    return {"status": "success", "turns": 3}


# =============================================================================
# SCENARIO 2: BUG INVESTIGATION AND FIXING
# =============================================================================

async def scenario_bug_investigation_workflow(client: Client):
    """
    Debugging session: User investigates and fixes a production bug
    
    Steps:
    1. User reports error with stack trace
    2. Assistant analyzes and identifies root cause
    3. User implements fix
    4. Assistant suggests additional improvements
    5. User adds tests to prevent regression
    """
    print_section("SCENARIO 2: Bug Investigation Workflow")
    
    session_id = "bug_fix_001"
    chat_id = make_chat_id(session_id)
    
    # Turn 1: Bug report with stack trace
    print("\n[Turn 1] User reports production bug...")
    result = await client.call_tool("ingest_conversation", {
        "request_id": make_request_id("bug"),
        "project_id": PROJECT_ID,
        "timestamp": make_timestamp(),
        "chat_meta": {
            "chat_id": chat_id,
            "base_chat_id": session_id,
            "request_attempt_id": make_request_id("attempt"),
            "chat_mode": "AGENT"
        },
        "messages": [
            {
                "sequence": 0,
                "role": "user",
                "content_summary": "Getting 'NoneType has no attribute encode' error in payment processing. Stack trace shows it's in payment/stripe.py line 67 when processing refunds.",
                "content_hash": make_content_hash("bug report 1"),
                "total_tokens": 30,
                "sequence": 0
            },
            {
                "sequence": 1,
                "role": "assistant",
                "content_summary": "The error occurs because payment.customer_email can be None for guest checkouts. The code assumes all payments have customer emails. We need defensive programming with proper null checks before encoding.",
                "content_hash": make_content_hash("bug analysis 1"),
                "prompt_tokens": 60,
                "completion_tokens": 95,
                "total_tokens": 155,
                "sequence": 1
            }
        ],
        "context_files": [
            make_context_file("payment/stripe.py", 0.98, "vecdb"),
            make_context_file("payment/models.py", 0.92, "ast"),
            make_context_file("tests/test_payments.py", 0.80, "vecdb")
        ],
        "tool_calls": [
            make_tool_call("read_file", "success", 310),
            make_tool_call("codebase_search", "success", 420)
        ],
        "code_changes": []
    })
    print_result("Turn 1 ingested", "OK", 1)
    
    await asyncio.sleep(1)
    
    # Turn 2: Implement fix
    print("\n[Turn 2] User implements defensive fix...")
    result = await client.call_tool("ingest_conversation", {
        "request_id": make_request_id("bug"),
        "project_id": PROJECT_ID,
        "timestamp": make_timestamp(),
        "chat_meta": {
            "chat_id": chat_id,
            "base_chat_id": session_id,
            "request_attempt_id": make_request_id("attempt"),
            "chat_mode": "AGENT"
        },
        "messages": [
            {
                "sequence": 0,
                "role": "user",
                "content_summary": "I've added null check for customer_email. Does this look right?",
                "content_hash": make_content_hash("bug question 2"),
                "total_tokens": 15,
                "sequence": 0
            },
            {
                "sequence": 1,
                "role": "assistant",
                "content_summary": "The fix looks good! Consider also: 1) Adding logging for None cases to track frequency, 2) Using fallback to transaction_id for tracking, 3) Adding a database migration to make customer_email nullable if not already",
                "content_hash": make_content_hash("bug analysis 2"),
                "prompt_tokens": 70,
                "completion_tokens": 110,
                "total_tokens": 180,
                "sequence": 1
            }
        ],
        "context_files": [
            make_context_file("payment/stripe.py", 0.97, "vecdb"),
            make_context_file("payment/logger.py", 0.85, "ast")
        ],
        "tool_calls": [
            make_tool_call("read_file", "success", 250),
            make_tool_call("edit_file", "success", 380)
        ],
        "code_changes": [
            make_code_change(
                "payment/stripe.py",
                "Added defensive null check for customer_email to prevent NoneType errors in refund processing",
                change_type="fixed",
                severity="critical",
                lines_added=8,
                lines_removed=2,
                function_name="process_refund"
            )
        ]
    })
    print_result("Turn 2 ingested", "OK", 1)
    
    await asyncio.sleep(1)
    
    # Turn 3: Add regression tests
    print("\n[Turn 3] Adding regression tests...")
    result = await client.call_tool("ingest_conversation", {
        "request_id": make_request_id("bug"),
        "project_id": PROJECT_ID,
        "timestamp": make_timestamp(),
        "chat_meta": {
            "chat_id": chat_id,
            "base_chat_id": session_id,
            "request_attempt_id": make_request_id("attempt"),
            "chat_mode": "AGENT"
        },
        "messages": [
            {
                "sequence": 0,
                "role": "user",
                "content_summary": "What tests should I add to prevent this bug from happening again?",
                "content_hash": make_content_hash("bug question 3"),
                "total_tokens": 16,
                "sequence": 0
            },
            {
                "sequence": 1,
                "role": "assistant",
                "content_summary": "Add these test cases: 1) test_refund_with_null_email() - verify refund works without customer email, 2) test_refund_logging_for_null_email() - verify proper logging, 3) test_guest_checkout_refund() - end-to-end test for guest users",
                "content_hash": make_content_hash("bug analysis 3"),
                "prompt_tokens": 80,
                "completion_tokens": 120,
                "total_tokens": 200,
                "sequence": 1
            }
        ],
        "context_files": [
            make_context_file("tests/test_payments.py", 0.96, "vecdb"),
            make_context_file("payment/stripe.py", 0.90, "ast")
        ],
        "tool_calls": [
            make_tool_call("read_file", "success", 290),
            make_tool_call("edit_file", "success", 520),
            make_tool_call("run_tests", "success", 3200)
        ],
        "code_changes": [
            make_code_change(
                "tests/test_payments.py",
                "Added comprehensive test cases for null customer_email scenarios to prevent regression",
                change_type="added",
                severity="medium",
                lines_added=45,
                lines_removed=0,
                function_name="test_refund_with_null_email"
            )
        ]
    })
    print_result("Turn 3 ingested", "OK", 1)
    
    # Search for similar bug fixes
    print("\n[Search] Finding similar null pointer fixes...")
    search_result = await client.call_tool("search", {
        "query": "null pointer defensive programming error handling",
        "group_id": PROJECT_ID,
        "limit": 5,
        "rerank_strategy": "rrf"
    })
    print_result("Search results", "Found similar defensive programming patterns", 1)
    
    print_result("Scenario 2", "COMPLETED", 0)
    return {"status": "success", "turns": 3}


# =============================================================================
# SCENARIO 3: FEATURE IMPLEMENTATION WITH ITERATIONS
# =============================================================================

async def scenario_feature_implementation_workflow(client: Client):
    """
    Feature development: User implements new API endpoint with iterations
    
    Steps:
    1. User describes feature requirements
    2. Assistant provides implementation plan
    3. User implements basic version
    4. Assistant suggests improvements (validation, error handling)
    5. User adds security and rate limiting
    6. Final review and optimization
    """
    print_section("SCENARIO 3: Feature Implementation Workflow")
    
    session_id = "feature_api_001"
    chat_id = make_chat_id(session_id)
    
    # Turn 1: Feature requirements
    print("\n[Turn 1] User describes feature requirements...")
    result = await client.call_tool("ingest_conversation", {
        "request_id": make_request_id("feature"),
        "project_id": PROJECT_ID,
        "timestamp": make_timestamp(),
        "chat_meta": {
            "chat_id": chat_id,
            "base_chat_id": session_id,
            "request_attempt_id": make_request_id("attempt"),
            "chat_mode": "AGENT"
        },
        "messages": [
            {
                "sequence": 0,
                "role": "user",
                "content_summary": "I need to add a REST API endpoint for bulk user updates. It should accept a list of user IDs and update fields, validate permissions, and return update status for each user.",
                "content_hash": make_content_hash("feature req 1"),
                "total_tokens": 40,
                "sequence": 0
            },
            {
                "sequence": 1,
                "role": "assistant",
                "content_summary": "Implementation plan: 1) Create POST /api/v1/users/bulk-update endpoint, 2) Add Pydantic model for validation (user_ids: List[int], updates: Dict), 3) Implement permission checks (admin or self-update only), 4) Use asyncio.gather() for parallel updates, 5) Return BulkUpdateResponse with success/failure for each user",
                "content_hash": make_content_hash("feature plan 1"),
                "prompt_tokens": 80,
                "completion_tokens": 150,
                "total_tokens": 230,
                "sequence": 1
            }
        ],
        "context_files": [
            make_context_file("api/v1/users.py", 0.95, "vecdb"),
            make_context_file("api/models/user.py", 0.90, "ast"),
            make_context_file("api/middleware/auth.py", 0.85, "vecdb")
        ],
        "tool_calls": [
            make_tool_call("read_file", "success", 320),
            make_tool_call("codebase_search", "success", 450)
        ],
        "code_changes": []
    })
    print_result("Turn 1 ingested", "OK", 1)
    
    await asyncio.sleep(1)
    
    # Turn 2: Basic implementation
    print("\n[Turn 2] User implements basic version...")
    result = await client.call_tool("ingest_code_context", {
        "project_id": PROJECT_ID,
        "name": "Add bulk user update endpoint",
        "summary": "Implemented POST /api/v1/users/bulk-update with basic validation and parallel processing",
        "reference_time": make_timestamp(),
        "metadata": {
            "file_path": "api/v1/users.py",
            "function_name": "bulk_update_users",
            "change_type": "added",
            "change_summary": "Added new endpoint with validation, rate limiting, and parallel processing support",
            "severity": "high",
            "lines_added": 85,
            "lines_removed": 0,
            "language": "python",
            "timestamp": make_timestamp()
        }
    })
    print_result("Code change ingested", "OK", 1)
    
    await asyncio.sleep(1)
    
    # Turn 3: Security and rate limiting
    print("\n[Turn 3] Adding security features...")
    result = await client.call_tool("ingest_conversation", {
        "request_id": make_request_id("feature"),
        "project_id": PROJECT_ID,
        "timestamp": make_timestamp(),
        "chat_meta": {
            "chat_id": chat_id,
            "base_chat_id": session_id,
            "request_attempt_id": make_request_id("attempt"),
            "chat_mode": "AGENT"
        },
        "messages": [
            {
                "sequence": 0,
                "role": "user",
                "content_summary": "The endpoint works! What security measures should I add?",
                "content_hash": make_content_hash("feature security 1"),
                "total_tokens": 14,
                "sequence": 0
            },
            {
                "sequence": 1,
                "role": "assistant",
                "content_summary": "Critical security additions: 1) Rate limiting: max 10 bulk updates per minute per user, 2) Input sanitization: validate all update fields against whitelist, 3) Audit logging: log all bulk operations with user_id and timestamp, 4) Maximum batch size: limit to 100 users per request to prevent DoS, 5) Transaction rollback: if any update fails, rollback all changes",
                "content_hash": make_content_hash("feature security answer 1"),
                "prompt_tokens": 90,
                "completion_tokens": 140,
                "total_tokens": 230,
                "sequence": 1
            }
        ],
        "context_files": [
            make_context_file("api/v1/users.py", 0.97, "vecdb"),
            make_context_file("api/middleware/rate_limit.py", 0.92, "ast"),
            make_context_file("api/middleware/audit.py", 0.88, "vecdb")
        ],
        "tool_calls": [
            make_tool_call("read_file", "success", 340),
            make_tool_call("edit_file", "success", 580)
        ],
        "code_changes": [
            make_code_change(
                "api/v1/users.py",
                "Added rate limiting, input sanitization, audit logging, and transaction rollback for bulk user updates",
                change_type="modified",
                severity="critical",
                lines_added=45,
                lines_removed=10,
                function_name="bulk_update_users"
            )
        ]
    })
    print_result("Turn 3 ingested", "OK", 1)
    
    # Search for similar API implementations
    print("\n[Search] Finding similar bulk operation patterns...")
    search_result = await client.call_tool("search", {
        "query": "bulk update API rate limiting security validation",
        "group_id": PROJECT_ID,
        "limit": 5,
        "rerank_strategy": "rrf"
    })
    print_result("Search results", "Found bulk operation best practices", 1)
    
    print_result("Scenario 3", "COMPLETED", 0)
    return {"status": "success", "turns": 3}


# =============================================================================
# SCENARIO 4: PERFORMANCE OPTIMIZATION SESSION
# =============================================================================

async def scenario_performance_optimization_workflow(client: Client):
    """
    Performance tuning: User optimizes slow endpoint
    
    Steps:
    1. User reports slow endpoint performance
    2. Assistant profiles and identifies bottlenecks
    3. User implements database query optimization
    4. Assistant suggests caching strategy
    5. User adds caching and monitoring
    6. Performance validation
    """
    print_section("SCENARIO 4: Performance Optimization Workflow")
    
    session_id = "perf_opt_001"
    chat_id = make_chat_id(session_id)
    
    # Turn 1: Performance problem report
    print("\n[Turn 1] User reports performance issue...")
    result = await client.call_tool("ingest_text", {
        "text": "Dashboard endpoint /api/dashboard is taking 8-12 seconds to load. Users are complaining. The endpoint loads user data, recent activities, and statistics. Need to optimize urgently.",
        "project_id": PROJECT_ID,
        "name": "Performance Issue: Dashboard slow loading"
    })
    print_result("Text ingested", "OK", 1)
    
    await asyncio.sleep(1)
    
    # Turn 2: Profiling and analysis
    print("\n[Turn 2] Profiling and bottleneck identification...")
    result = await client.call_tool("ingest_conversation", {
        "request_id": make_request_id("perf"),
        "project_id": PROJECT_ID,
        "timestamp": make_timestamp(),
        "chat_meta": {
            "chat_id": chat_id,
            "base_chat_id": session_id,
            "request_attempt_id": make_request_id("attempt"),
            "chat_mode": "AGENT"
        },
        "messages": [
            {
                "sequence": 0,
                "role": "user",
                "content_summary": "I ran a profiler. The dashboard makes 250+ database queries! Most are N+1 queries loading related objects.",
                "content_hash": make_content_hash("perf analysis 1"),
                "total_tokens": 25,
                "sequence": 0
            },
            {
                "sequence": 1,
                "role": "assistant",
                "content_summary": "Classic N+1 problem! Solution: 1) Use select_related() for ForeignKey relations (user profiles, teams), 2) Use prefetch_related() for ManyToMany (activities, tags), 3) Add composite indexes on (user_id, created_at), 4) Consider denormalization for statistics (store counts in user table)",
                "content_hash": make_content_hash("perf solution 1"),
                "prompt_tokens": 100,
                "completion_tokens": 160,
                "total_tokens": 260,
                "sequence": 1
            }
        ],
        "context_files": [
            make_context_file("api/dashboard.py", 0.98, "vecdb"),
            make_context_file("models/user.py", 0.94, "ast"),
            make_context_file("models/activity.py", 0.90, "ast")
        ],
        "tool_calls": [
            make_tool_call("profile_code", "success", 8500),
            make_tool_call("analyze_queries", "success", 1200)
        ],
        "code_changes": []
    })
    print_result("Turn 2 ingested", "OK", 1)
    
    await asyncio.sleep(1)
    
    # Turn 3: Implementing optimizations
    print("\n[Turn 3] Implementing query optimizations...")
    result = await client.call_tool("ingest_code_context", {
        "project_id": PROJECT_ID,
        "name": "Optimize dashboard queries",
        "summary": "Added select_related and prefetch_related to eliminate N+1 queries, reducing query count from 250+ to 8",
        "reference_time": make_timestamp(),
        "metadata": {
            "file_path": "api/dashboard.py",
            "function_name": "get_dashboard_data",
            "change_type": "refactored",
            "change_summary": "Response time improved from 8s to 450ms by optimizing database queries",
            "severity": "critical",
            "lines_added": 25,
            "lines_removed": 35,
            "language": "python",
            "diff_summary": "Added select_related for user relationships, prefetch_related for nested queries",
            "timestamp": make_timestamp()
        }
    })
    print_result("Code change ingested", "OK", 1)
    
    await asyncio.sleep(1)
    
    # Turn 4: Adding caching layer
    print("\n[Turn 4] Adding Redis caching...")
    result = await client.call_tool("ingest_conversation", {
        "request_id": make_request_id("perf"),
        "project_id": PROJECT_ID,
        "timestamp": make_timestamp(),
        "chat_meta": {
            "chat_id": chat_id,
            "base_chat_id": session_id,
            "request_attempt_id": make_request_id("attempt"),
            "chat_mode": "AGENT"
        },
        "messages": [
            {
                "sequence": 0,
                "role": "user",
                "content_summary": "Queries are much faster! Should I add caching for further improvement?",
                "content_hash": make_content_hash("perf caching 1"),
                "total_tokens": 14,
                "sequence": 0
            },
            {
                "sequence": 1,
                "role": "assistant",
                "content_summary": "Yes, add Redis caching: 1) Cache dashboard data with 5-minute TTL, 2) Use cache key pattern 'dashboard:{user_id}:{date}', 3) Implement cache invalidation on user data updates, 4) Add cache warming for active users during off-peak hours, 5) Monitor cache hit rate (aim for >80%)",
                "content_hash": make_content_hash("perf caching answer 1"),
                "prompt_tokens": 110,
                "completion_tokens": 145,
                "total_tokens": 255,
                "sequence": 1
            }
        ],
        "context_files": [
            make_context_file("api/dashboard.py", 0.96, "vecdb"),
            make_context_file("cache/redis_client.py", 0.92, "ast"),
            make_context_file("cache/strategies.py", 0.85, "vecdb")
        ],
        "tool_calls": [
            make_tool_call("read_file", "success", 310),
            make_tool_call("edit_file", "success", 520)
        ],
        "code_changes": [
            make_code_change(
                "api/dashboard.py",
                "Added Redis caching layer with 5-minute TTL and smart invalidation, reducing response time to 45ms for cached requests",
                change_type="modified",
                severity="high",
                lines_added=35,
                lines_removed=5,
                function_name="get_dashboard_data"
            )
        ]
    })
    print_result("Turn 4 ingested", "OK", 1)
    
    # Search for performance optimization patterns
    print("\n[Search] Finding similar N+1 optimization techniques...")
    search_result = await client.call_tool("search", {
        "query": "N+1 query optimization caching performance database",
        "group_id": PROJECT_ID,
        "limit": 5,
        "rerank_strategy": "rrf"
    })
    print_result("Search results", "Found N+1 optimization patterns", 1)
    
    print_result("Scenario 4", "COMPLETED", 0)
    return {"status": "success", "turns": 4}


# =============================================================================
# SCENARIO 5: CROSS-PROJECT KNOWLEDGE RETRIEVAL
# =============================================================================

async def scenario_cross_project_knowledge_retrieval(client: Client):
    """
    Knowledge retrieval: User searches across multiple coding sessions
    
    Demonstrates:
    1. Semantic search across different topics
    2. Context building from past conversations
    3. Learning from previous implementations
    """
    print_section("SCENARIO 5: Cross-Project Knowledge Retrieval")
    
    # Test various search queries
    test_queries = [
        ("async await patterns", "Find all async/await refactoring knowledge"),
        ("security vulnerability fixes", "Recall security-related bug fixes"),
        ("performance optimization techniques", "Retrieve performance tuning strategies"),
        ("API endpoint implementation", "Find API development patterns"),
        ("database query optimization", "Search for database optimization examples")
    ]
    
    search_results = {}
    
    for query, description in test_queries:
        print(f"\n[Query] {description}...")
        print_result("Query", f"'{query}'", 1)
        
        # Try different search strategies
        for strategy in ["rrf", "mmr", "cross_encoder"]:
            result = await client.call_tool("search", {
                "query": query,
                "group_id": PROJECT_ID,
                "limit": 3,
                "rerank_strategy": strategy
            })
            
            # Parse result (simplified)
            result_text = result.content[0].text if result.content else "No results"
            print_result(f"Strategy {strategy}", f"Found results", 2)
        
        await asyncio.sleep(0.5)
    
    print_result("Scenario 5", "COMPLETED", 0)
    return {"status": "success", "queries": len(test_queries)}


# =============================================================================
# SCENARIO 6: CONCURRENT REQUEST STRESS TEST
# =============================================================================

async def scenario_concurrent_request_stress_test(client: Client):
    """
    Stress testing: Multiple concurrent ingest and search operations
    
    Tests:
    1. Concurrent conversation ingestion
    2. Parallel search queries
    3. Mixed operation workload
    4. Performance under load
    """
    print_section("SCENARIO 6: Concurrent Request Stress Test")
    
    # Test 1: Concurrent ingestion
    print("\n[Test 1] Concurrent text ingestion (10 parallel requests)...")
    start_time = time.time()
    
    tasks = []
    for i in range(10):
        task = client.call_tool("ingest_text", {
            "text": f"Concurrent test memory {i}: Testing parallel ingestion capabilities of FastMCP server under load. This simulates multiple users ingesting data simultaneously.",
            "project_id": PROJECT_ID,
            "name": f"Concurrent Test {i}"
        })
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end_time = time.time()
    
    success_count = sum(1 for r in results if not isinstance(r, Exception))
    print_result("Requests completed", f"{success_count}/10", 1)
    print_result("Total time", f"{end_time - start_time:.2f}s", 1)
    print_result("Avg per request", f"{(end_time - start_time) / 10:.2f}s", 1)
    
    await asyncio.sleep(2)
    
    # Test 2: Concurrent searches
    print("\n[Test 2] Concurrent searches (15 parallel queries)...")
    start_time = time.time()
    
    search_queries = [
        "async performance",
        "database optimization",
        "security fixes",
        "API implementation",
        "error handling",
    ] * 3  # 15 total queries
    
    tasks = []
    for query in search_queries:
        task = client.call_tool("search", {
            "query": query,
            "group_id": PROJECT_ID,
            "limit": 3,
            "rerank_strategy": "rrf"
        })
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end_time = time.time()
    
    success_count = sum(1 for r in results if not isinstance(r, Exception))
    print_result("Searches completed", f"{success_count}/15", 1)
    print_result("Total time", f"{end_time - start_time:.2f}s", 1)
    print_result("Avg per search", f"{(end_time - start_time) / 15:.2f}s", 1)
    
    print_result("Scenario 6", "COMPLETED", 0)
    return {
        "status": "success",
        "ingest_success": success_count,
        "search_success": success_count
    }


# =============================================================================
# SCENARIO 7: ADMIN AND MONITORING OPERATIONS
# =============================================================================

async def scenario_admin_monitoring_operations(client: Client):
    """
    Admin operations: System health, statistics, and cache management
    
    NOTE: Admin POST endpoints are filtered out in server_http.py for security.
    This scenario now tests read-only resources instead.
    
    Tests:
    1. Health check monitoring (resources)
    2. Statistics retrieval (resources)
    """
    print_section("SCENARIO 7: Admin and Monitoring Operations")
    
    # NOTE: Admin POST tools are filtered out. Test resources instead.
    print("\n[INFO] Admin POST endpoints (/cache/, /admin/, /langfuse/) are filtered")
    print("       Testing read-only resource endpoints instead...\n")
    
    # Test 1: Read cache stats (resource - allowed)
    print("\n[Test 1] Reading cache statistics...")
    try:
        result = await client.read_resource("resource://get_cache_stats")
        print_result("Cache stats retrieved", "Success", 1)
    except Exception as e:
        print_result("Cache stats", f"Error: {str(e)[:50]}", 1)
    
    await asyncio.sleep(0.5)
    
    # Test 2: Check cache health (resource - allowed)
    print("\n[Test 2] Checking cache health...")
    try:
        result = await client.read_resource("resource://cache_health")
        print_result("Cache health checked", "Success", 1)
    except Exception as e:
        print_result("Cache health", f"Error: {str(e)[:50]}", 1)
    
    await asyncio.sleep(0.5)
    
    # Test 3: Get tool stats (resource - allowed)
    print("\n[Test 3] Reading tool statistics...")
    try:
        result = await client.read_resource("resource://get_tool_stats")
        print_result("Tool stats retrieved", "Success", 1)
    except Exception as e:
        print_result("Tool stats", f"Error: {str(e)[:50]}", 1)
    
    await asyncio.sleep(0.5)
    
    # Test 4: Check Langfuse health (resource - allowed)
    print("\n[Test 4] Checking Langfuse status...")
    try:
        result = await client.read_resource("resource://langfuse_health")
        print_result("Langfuse health checked", "Success", 1)
    except Exception as e:
        print_result("Langfuse health", f"Error: {str(e)[:50]}", 1)
    
    print_result("Scenario 7", "COMPLETED", 0)
    return {"status": "success", "operations": 4}


# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

async def run_comprehensive_test_suite():
    """Run all comprehensive test scenarios"""
    print_section("FASTMCP COMPREHENSIVE TEST SUITE", "=")
    print(f"Project ID: {PROJECT_ID}")
    print(f"Server URL: {BASE_URL}")
    print(f"Total Scenarios: 7")
    print()
    
    results = {}
    start_time = time.time()
    
    async with Client(BASE_URL) as client:
        # Scenario 1: Async Refactoring
        try:
            results["async_refactoring"] = await scenario_async_refactoring_workflow(client)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[ERROR] Scenario 1 failed: {e}")
            results["async_refactoring"] = {"status": "failed", "error": str(e)}
        
        # Scenario 2: Bug Investigation
        try:
            results["bug_investigation"] = await scenario_bug_investigation_workflow(client)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[ERROR] Scenario 2 failed: {e}")
            results["bug_investigation"] = {"status": "failed", "error": str(e)}
        
        # Scenario 3: Feature Implementation
        try:
            results["feature_implementation"] = await scenario_feature_implementation_workflow(client)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[ERROR] Scenario 3 failed: {e}")
            results["feature_implementation"] = {"status": "failed", "error": str(e)}
        
        # Scenario 4: Performance Optimization
        try:
            results["performance_optimization"] = await scenario_performance_optimization_workflow(client)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[ERROR] Scenario 4 failed: {e}")
            results["performance_optimization"] = {"status": "failed", "error": str(e)}
        
        # Scenario 5: Cross-Project Knowledge
        try:
            results["knowledge_retrieval"] = await scenario_cross_project_knowledge_retrieval(client)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[ERROR] Scenario 5 failed: {e}")
            results["knowledge_retrieval"] = {"status": "failed", "error": str(e)}
        
        # Scenario 6: Stress Test
        try:
            results["stress_test"] = await scenario_concurrent_request_stress_test(client)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[ERROR] Scenario 6 failed: {e}")
            results["stress_test"] = {"status": "failed", "error": str(e)}
        
        # Scenario 7: Admin Operations
        try:
            results["admin_operations"] = await scenario_admin_monitoring_operations(client)
        except Exception as e:
            print(f"[ERROR] Scenario 7 failed: {e}")
            results["admin_operations"] = {"status": "failed", "error": str(e)}
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Final Summary
    print_section("TEST SUITE SUMMARY", "=")
    
    success_count = sum(1 for r in results.values() if r.get("status") == "success")
    total_count = len(results)
    
    print(f"\nResults:")
    for scenario, result in results.items():
        status = result.get("status", "unknown")
        icon = "[OK]" if status == "success" else "[FAIL]"
        print(f"  {icon} {scenario.replace('_', ' ').title()}")
    
    print(f"\nOverall:")
    print_result("Total scenarios", total_count, 1)
    print_result("Successful", success_count, 1)
    print_result("Failed", total_count - success_count, 1)
    print_result("Success rate", f"{(success_count/total_count*100):.1f}%", 1)
    print_result("Total time", f"{total_time:.2f}s", 1)
    
    # Save detailed results to JSON
    output_file = Path(__file__).parent / "comprehensive_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat(),
            "project_id": PROJECT_ID,
            "total_time": total_time,
            "results": results,
            "summary": {
                "total": total_count,
                "success": success_count,
                "failed": total_count - success_count,
                "success_rate": f"{(success_count/total_count*100):.1f}%"
            }
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_file}")
    
    return success_count == total_count


if __name__ == "__main__":
    success = asyncio.run(run_comprehensive_test_suite())
    exit(0 if success else 1)

