"""
HTTP MCP Server - Auto-generated from FastAPI
==============================================
Runs the MCP server as an HTTP server instead of stdio mode.
This allows for HTTP streaming and easier testing.
"""

from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType
import sys
import os
import uvicorn

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add memory_layer to Python path
memory_layer_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "memory_layer"))
sys.path.insert(0, memory_layer_path)

# Import the FastAPI app from memory_layer
from app.main import app as fastapi_app

print(f"[OK] Loaded FastAPI app from memory_layer: {fastapi_app.title}")

# ============================================================================
# CONVERT FASTAPI TO MCP SERVER
# ============================================================================

# Define route filter function to exclude admin endpoints
def should_include_route(route) -> bool:
    """
    Filter function to exclude admin/maintenance endpoints from MCP
    
    Returns False for routes we want to SKIP
    Returns True for routes we want to INCLUDE
    """
    path = route.path
    method = route.methods
    
    # Skip admin/maintenance POST endpoints
    admin_patterns = [
        '/cache/',
        '/admin/',
        '/langfuse/',
        '/config/',
        '/innocody/'
    ]
    
    if 'POST' in method:
        for pattern in admin_patterns:
            if pattern in path:
                print(f"[SKIP] Excluding admin endpoint: POST {path}")
                return False
    
    # Include all other routes
    return True

# Filter FastAPI routes before conversion
from starlette.routing import Route
filtered_routes = [route for route in fastapi_app.routes if should_include_route(route)]

# Create filtered FastAPI app
from fastapi import FastAPI
filtered_app = FastAPI(
    title=fastapi_app.title,
    description=fastapi_app.description,
    version=fastapi_app.version,
    routes=filtered_routes,
    lifespan=fastapi_app.router.lifespan_context
)

# Define custom route mapping rules (for filtered app)
custom_route_maps = [
    # GET with path params → ResourceTemplates
    RouteMap(
        methods=["GET"],
        pattern=r".*\{.*\}.*",
        mcp_type=MCPType.RESOURCE_TEMPLATE
    ),
    # Other GET → Resources
    RouteMap(
        methods=["GET"],
        pattern=r".*",
        mcp_type=MCPType.RESOURCE
    ),
    # POST/PUT/DELETE → Tools (default behavior)
]

# Convert filtered FastAPI app to MCP server
mcp = FastMCP.from_fastapi(
    app=filtered_app,
    name="ZepAI Memory Layer",
    route_maps=custom_route_maps
)

print(f"[OK] Created MCP server: {mcp.name}")
print(f"     Original endpoints: {len(fastapi_app.routes)}")
print(f"     Filtered endpoints: {len(filtered_routes)}")
print(f"     Excluded endpoints: {len(fastapi_app.routes) - len(filtered_routes)}")

# ============================================================================
# CUSTOM TOOLS (Optional - currently empty)
# ============================================================================
# All tools are auto-generated from FastAPI endpoints via FastMCP.from_fastapi()
# This keeps the codebase simple and avoids redundant wrapper functions.
# Users can call the auto-generated tools directly with appropriate parameters.
# ============================================================================


# ============================================================================
# HTTP SERVER SETUP
# ============================================================================

def create_http_app():
    """
    Create HTTP app using COMBINED ROUTES pattern from FastMCP docs
    Reference: https://gofastmcp.com/integrations/fastapi#offering-an-llm-friendly-api
    
    This pattern combines MCP routes and FastAPI routes into a single app.
    """
    from fastapi import FastAPI
    
    # Create the MCP's ASGI app with '/mcp' path
    mcp_app = mcp.http_app(path='/mcp')
    
    # Create a new FastAPI app that combines both sets of routes
    combined_app = FastAPI(
        title="ZepAI Memory Layer with MCP",
        description="FastAPI + MCP Server - Auto-generated from memory_layer",
        version="2.0.0",
        routes=[
            *mcp_app.routes,      # MCP routes at /mcp/*
            *fastapi_app.routes,  # Original API routes
        ],
        lifespan=mcp_app.lifespan,  # Important: use MCP lifespan
    )
    
    print(f"\n[OK] Combined MCP routes and FastAPI routes")
    print(f"[OK] Total routes: {len(combined_app.routes)}")
    
    return combined_app

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("FastMCP HTTP Server - Auto-generated from FastAPI")
    print("="*70)
    print(f"\nServer ready!")
    print(f"  - Name: {mcp.name}")
    print(f"  - Total routes converted: {len(fastapi_app.routes)}")
    print(f"\nHTTP Endpoints:")
    print(f"  - MCP Server (SSE): http://localhost:8002/mcp/sse")
    print(f"  - MCP Server (Messages): http://localhost:8002/mcp/messages")
    print(f"  - Original FastAPI Docs: http://localhost:8002/docs")
    print(f"  - Root API: http://localhost:8002/")
    print(f"\nTo test:")
    print(f"  1. FastAPI docs: http://localhost:8002/docs")
    print(f"  2. MCP via SSE: curl http://localhost:8002/mcp/sse")
    print(f"  3. Connect MCP client to: http://localhost:8002/mcp")
    print(f"\nNote: FastMCP uses Server-Sent Events (SSE), not a web UI inspector.")
    print("\n" + "="*70)
    
    # Create HTTP app
    http_app = create_http_app()
    
    print("\nStarting HTTP MCP server on port 8002...")
    print("Press Ctrl+C to stop\n")
    
    # Run with uvicorn
    uvicorn.run(
        http_app,
        host="0.0.0.0",
        port=8002,
        log_level="info"
    )
