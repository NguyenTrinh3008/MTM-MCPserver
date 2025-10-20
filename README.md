# FastMCP 2.0 Server - ZepAI Memory Layer

Auto-generated MCP server từ FastAPI backend sử dụng [FastMCP 2.0](https://github.com/jlowin/fastmcp)

## 🏗️ **Architecture**

Server này sử dụng `FastMCP.from_fastapi()` để tự động convert tất cả endpoints từ FastAPI app (`memory_layer`) thành MCP tools và resources.

**Key Components:**
- **`server_http.py`** - Main MCP server file, auto-generates tools từ FastAPI endpoints
- **`memory_layer/`** - FastAPI backend (required dependency, not included in this repo)
- **`config.py`** - Configuration settings
- **`test/`** - Test suite and examples

## 🚀 **Features**

### **Auto-generated MCP Tools:**

All tools are **automatically generated** from FastAPI POST endpoints:

**🔍 Search Tools:**
- `search` - Semantic search với reranking strategies
- `search_code` - Search code changes với metadata filters

**📥 Ingest Tools:**
- `ingest_text` - Ingest plain text vào knowledge graph
- `ingest_message` - Ingest conversation messages
- `ingest_json` - Ingest structured JSON data
- `ingest_code` - Ingest code changes với LLM importance scoring
- `ingest_code_context` - Ingest advanced code metadata với TTL
- `ingest_conversation` - Ingest full conversation context

**📊 Admin Tools (Read-only):**
- Admin **POST** endpoints are **filtered out** for safety
- Only **GET** endpoints are exposed as MCP Resources
- Includes: stats, cache info, health checks

### **Auto-generated MCP Resources:**

All GET endpoints with path parameters become Resource Templates:

## 📦 **Installation**

### **Prerequisites:**

1. **memory_layer** FastAPI backend phải running tại `http://localhost:8000`
2. Folder structure:
   ```
   ZepAI/
   ├── memory_layer/          # FastAPI backend (required)
   │   └── app/
   │       └── main.py        # Contains FastAPI app
   └── fastmcp_server/        # This repository
       ├── server_http.py
       ├── config.py
       └── requirements.txt
   ```

### **Install Dependencies:**

```bash
cd fastmcp_server
pip install -r requirements.txt

# Or with uv
uv pip install -r requirements.txt
```

## ⚙️ **Configuration**

Create `.env` file (optional, có defaults):

```env
# Memory Layer Backend URL
MEMORY_LAYER_URL=http://localhost:8000
MEMORY_LAYER_TIMEOUT=30

# Default Settings
DEFAULT_PROJECT_ID=default_project
MAX_SEARCH_RESULTS=50
MAX_TEXT_LENGTH=100000
MAX_CONVERSATION_MESSAGES=100
```

## 🏃 **Running the Server**

### **1. Start memory_layer backend first:**
```bash
cd ../memory_layer
python -m uvicorn app.main:app --port 8000
```

### **2. Start MCP server:**
```bash
cd ../fastmcp_server
python server_http.py
```

Server will run on `http://localhost:8002`

## 📡 **Available Endpoints**

Combined FastAPI + MCP routes:

**MCP Endpoints (at /mcp):**
- `GET /mcp/sse` - Server-Sent Events connection
- `POST /mcp/messages` - MCP message endpoint
- MCP Client connection: `http://localhost:8002/mcp`

**Original FastAPI Routes:**
- `GET /docs` - OpenAPI documentation
- `GET /` - API root and health check
- All original endpoints from memory_layer

**Key MCP Paths:**
- Tools list: Call via MCP client
- Resources list: Call via MCP client
- Test connection: `curl http://localhost:8002/mcp/sse`

## 🧪 **Testing**

### **Run Test Suite:**

```bash
cd test
python test_client.py
```

Test suite includes:
- Basic functionality tests
- Tool calling tests
- Resource reading tests
- Search and ingest workflows
- Comprehensive scenario tests

### **Using FastMCP Client:**

```python
from fastmcp import Client
import asyncio

async def test():
    # Connect to server
    async with Client("http://localhost:8002/mcp") as client:
        # List tools
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")
        
        # List resources
        resources = await client.list_resources()
        print(f"Available resources: {[r.uri for r in resources]}")
        
        # Call a tool (auto-generated from FastAPI)
        result = await client.call_tool("ingest_text", {
            "text": "Test content",
            "project_id": "test_project"
        })
        print(f"Result: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(test())
```

### **Using curl:**

```bash
# Test SSE connection
curl http://localhost:8002/mcp/sse

# Access FastAPI docs
curl http://localhost:8002/docs
```

## 📊 **Comparison: FastMCP vs Custom Implementation**

| Aspect | Custom MCP | FastMCP 2.0 (Auto-generated) |
|--------|-----------|-------------|
| **Lines of Code** | ~2,900 | ~180 (94% reduction) |
| **Setup Time** | 5 weeks | 1 day |
| **Tools Definition** | Manual (11 tools) | Auto-generated from FastAPI |
| **Tools Registration** | Manual (254 lines) | Automatic via `from_fastapi()` |
| **Validation** | Manual Pydantic | Inherits from FastAPI |
| **Transport** | Custom HTTP+SSE | Built-in HTTP/SSE |
| **Error Handling** | Manual | Automatic |
| **Testing** | Custom client | FastMCP Client + test suite |
| **Maintenance** | Update 2 places | Update FastAPI only |
| **Deployment** | Complex | `python server_http.py` |

## 🔄 **How It Works**

### **Auto-conversion Process:**

```python
# 1. Import FastAPI app from memory_layer
from app.main import app as fastapi_app

# 2. Filter routes (exclude admin POST endpoints)
filtered_routes = [route for route in fastapi_app.routes 
                   if should_include_route(route)]

# 3. Auto-convert to MCP server
mcp = FastMCP.from_fastapi(
    app=filtered_app,
    name="ZepAI Memory Layer",
    route_maps=custom_route_maps  # GET with params → Resources
)

# 4. Combine MCP + original FastAPI routes
combined_app = FastAPI(
    routes=[
        *mcp_app.routes,      # MCP at /mcp/*
        *fastapi_app.routes,  # Original API
    ]
)
```

### **Route Mapping Rules:**

1. **POST/PUT/DELETE** → MCP Tools (writable operations)
2. **GET with `{params}`** → MCP Resource Templates (dynamic data)
3. **GET without params** → MCP Resources (static data)
4. **Admin POST endpoints** → Filtered out (safety)

### **Benefits:**

✅ **Single source of truth** - Update FastAPI, MCP updates automatically  
✅ **No code duplication** - Tools inherit FastAPI validation  
✅ **Type safety** - Pydantic models from FastAPI = MCP schemas  
✅ **Zero maintenance** - Add new FastAPI endpoint = new MCP tool automatically  
✅ **Combined access** - Use via MCP client OR direct HTTP/OpenAPI

## 🎯 **Key Design Decisions**

### **1. Why Auto-generation?**
- **DRY principle** - FastAPI already defines all endpoints, schemas, validation
- **Zero maintenance** - No manual tool registration needed
- **Type safety** - Inherits Pydantic validation from FastAPI

### **2. Why Filter Admin Endpoints?**
- **Safety** - Prevent accidental cache clearing via MCP client
- **Read-only monitoring** - Admin GET endpoints still exposed as resources
- **Explicit control** - Destructive operations require direct API access

### **3. Why Combined Routes?**
- **Flexibility** - Access via MCP client OR OpenAPI/Swagger
- **Debugging** - Use `/docs` for quick endpoint testing
- **Migration path** - Existing API clients continue working

### **4. File Structure:**
```
fastmcp_server/
├── server_http.py              # Main server (180 lines)
├── config.py                   # Configuration
├── memory_client.py            # Legacy (not used anymore)
├── search_results_formatter.py # Result formatting utilities
├── requirements.txt            # Dependencies
├── .env                        # Environment config (gitignored)
└── test/                       # Test suite
    ├── test_client.py          # Basic tests
    ├── test_comprehensive_scenarios.py
    └── test_search_analysis.py
```

## 📖 **Documentation**

- [FastMCP Documentation](https://gofastmcp.com)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)

## 🎯 **Benefits of This Approach**

✅ **94% less code** - 180 lines vs 2,900 lines  
✅ **Zero tool registration** - Auto-generated from FastAPI  
✅ **Single source of truth** - Update FastAPI once  
✅ **Type-safe** - Inherits Pydantic validation  
✅ **Dual access** - MCP client OR OpenAPI/Swagger  
✅ **Easy testing** - Built-in test utilities + `/docs`  
✅ **Safe by default** - Admin operations filtered  
✅ **Future-proof** - New FastAPI endpoints = new MCP tools automatically  

## 🔗 **Links**

- [FastMCP Documentation](https://gofastmcp.com)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📝 **License**

Same as original project.

---

**Note:** This server requires the `memory_layer` FastAPI backend to be running. The MCP server acts as a protocol adapter, exposing FastAPI endpoints as MCP tools and resources.


