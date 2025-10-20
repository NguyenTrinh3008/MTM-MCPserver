# FastMCP 2.0 Server - ZepAI Memory Layer

Migration từ custom MCP implementation sang [FastMCP 2.0](https://github.com/jlowin/fastmcp)

## 🚀 **Features**

### **8 Core MCP Tools (Auto-generated from FastAPI):**

**🔍 Search Tools (2):**
- `search` - Semantic search với reranking strategies (supports LLM classification via `use_llm_classification=true`)
- `search_code` - Search code changes với metadata filters

**📥 Ingest Tools (6):**
- `ingest_text` - Ingest plain text vào knowledge graph
- `ingest_message` - Ingest conversation messages
- `ingest_json` - Ingest structured JSON data
- `ingest_code` - Ingest simple code change với LLM importance scoring
- `ingest_code_context` - Ingest advanced code metadata với TTL + relationships
- `ingest_conversation` - Ingest full conversation context (at `/conversation/ingest`)

**📊 Admin & Analytics:**
- All admin tools are auto-generated from FastAPI GET endpoints (Resources)
- Cache management, stats, debugging endpoints available via MCP resources

### **7 MCP Resources:**
- `memory://conversations/{project_id}` - Conversation memories
- `memory://stats/{project_id}` - Project statistics

## 📦 **Installation**

```bash
# Install dependencies
pip install -r requirements.txt

# Or with uv
uv pip install -r requirements.txt
```

## ⚙️ **Configuration**

Create `.env` file:

```env
MEMORY_LAYER_URL=http://localhost:8000
MEMORY_LAYER_TIMEOUT=30
DEFAULT_PROJECT_ID=default_project
MAX_SEARCH_RESULTS=50
MAX_TEXT_LENGTH=100000
MAX_CONVERSATION_MESSAGES=100
```

## 🏃 **Running the Server**

### **HTTP Transport (Default):**
```bash
python server.py
```

Server will run on `http://localhost:8001`

### **Stdio Transport:**
```python
# In server.py, change:
mcp.run(transport="stdio")
```

### **With FastMCP CLI:**
```bash
fastmcp run server.py
```

## 📡 **Available Endpoints**

When running with HTTP transport:

- `GET /health` - Health check
- `POST /mcp/tools/call` - Call MCP tools
- `GET /mcp/tools/list` - List available tools
- `POST /mcp/resources/read` - Read MCP resources
- `GET /mcp/resources/list` - List available resources

## 🧪 **Testing**

### **Using FastMCP Client:**

```python
from fastmcp import Client
import asyncio

async def test():
    # Connect to server
    async with Client("http://localhost:8001/mcp") as client:
        # List tools
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")
        
        # Call a tool
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
# List tools
curl http://localhost:8001/mcp/tools/list

# Call tool
curl -X POST http://localhost:8001/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "search_knowledge",
    "arguments": {
      "query": "async performance",
      "project_id": "test_project",
      "limit": 5
    }
  }'
```

## 📊 **Comparison: FastMCP vs Custom Implementation**

| Aspect | Custom MCP | FastMCP 2.0 (Consolidated) |
|--------|-----------|-------------|
| **Lines of Code** | ~2,900 | ~540 (81% reduction) |
| **Setup Time** | 5 weeks | 3 days |
| **Core Tools** | 11 (with wrappers) | 8 (auto-generated only) |
| **Tools Registration** | Manual (254 lines) | Auto-conversion (0 lines) |
| **Validation** | Manual Pydantic | Automatic |
| **Transport** | Custom HTTP+SSE | Built-in HTTP/SSE/Stdio |
| **Error Handling** | Manual | Automatic |
| **Testing** | Custom client | Built-in utilities |
| **Deployment** | Complex | Simple |

## 🔄 **Migration Notes**

### **What Changed:**

1. **No Transport Layer** - FastMCP handles it automatically
2. **No Manual Registration** - Use `@mcp.tool()` decorator (or auto-conversion via `FastMCP.from_fastapi()`)
3. **No Custom Validators** - Type hints = validation
4. **No HTTP Endpoints** - FastMCP creates them automatically
5. **Simpler Error Handling** - Return strings, FastMCP formats errors
6. **No Custom Wrapper Tools** - Removed `smart_search` and `quick_code_search`:
   - Use `search` with `use_llm_classification=true` instead of `smart_search`
   - Use `search_code` directly instead of `quick_code_search`
7. **Consolidated Endpoints** - Removed duplicate `/ingest/conversation`, use `/conversation/ingest`

### **What Stayed the Same:**

1. **Memory Client** - Same HTTP client logic
2. **Business Logic** - Same tool implementations
3. **Backend Communication** - Same endpoints
4. **Configuration** - Similar config structure

## 🚀 **Next Steps**

1. **Add Authentication:**
   ```python
   from fastmcp.server.auth import GoogleProvider
   
   auth = GoogleProvider(
       client_id="...",
       client_secret="...",
       base_url="https://myserver.com"
   )
   mcp = FastMCP("Protected Server", auth=auth)
   ```

2. **Deploy to FastMCP Cloud:**
   ```bash
   fastmcp deploy server.py
   ```

3. **Add More Resources:**
   ```python
   @mcp.resource("memory://code/{project_id}")
   async def code_memories(project_id: str):
       # Implementation
       pass
   ```

## 📖 **Documentation**

- [FastMCP Documentation](https://gofastmcp.com)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)

## 🎯 **Benefits of FastMCP**

✅ **80% less code** - Focus on business logic  
✅ **Faster development** - 3 days vs 5 weeks  
✅ **Built-in HTTP** - No manual transport implementation  
✅ **Automatic validation** - Type hints = validation  
✅ **Better testing** - Built-in test utilities  
✅ **Easy deployment** - One command  
✅ **Production ready** - Battle-tested library  
✅ **Community support** - Active development  

## 📝 **License**

Same as original project.


