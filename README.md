# Context Writer

A blog writing tool built with FastHTML and nbdev, designed for literate programming and progressive feature development.

## 🚀 Quick Start

### Prerequisites
1. Install [ruler](https://okigu.com/ruler): `npm install -g @intellectronica/ruler` (manages AI agent configuration and MCP server setup)
2. Install [fastmcp](https://gofastmcp.com/getting-started/installation): `uv pip install fastmcp` (required by the custom MCP server)

### Setup
1. **Clone and configure environment:**
   ```bash
   git clone git@github.com:DavidFarrell/context_writer.git
   cd context_writer
   
   # IMPORTANT: Set up your API keys
   cp .env.example .env
   # Edit .env and add your OpenAI API key and gemini key
   ```

2. **Configure Ruler (IMPORTANT):**
   ```bash
   # Copy the example ruler config
   cp .ruler/ruler.toml.example .ruler/ruler.toml
   
   # Edit .ruler/ruler.toml and replace the X's with your actual OpenAI API key from .env
   # The key should look like: sk-proj-XXXX... → sk-proj-YourActualKeyHere...
   ```

3. **Apply Ruler context to your AI agents:**
   ```bash
   ruler apply  # Applies to: copilot, claude, codex, cursor, gemini-cli, opencode, qwen (as configured)
   # OR override to specific agents:
   ruler apply --agents claude,cursor
   ```
   
   **Note:** Ruler automatically configures MCP servers in each AI tool's configuration file (e.g., `.mcp.json` for Claude Code, `.cursor/mcp.json` for Cursor, etc.)

4. **Verify MCP connection in Claude Code:**
   ```
   /mcp
   ```
   You should see `fasthtml-tester` in the list of connected servers.

## 📁 Project Structure

```
context_writer/
├── .ruler/           # AI agent context and guidelines
│   ├── AGENTS.md     # Project overview and development philosophy
│   ├── api_conventions_monsterui.md  # UI component reference
│   ├── fast_html_best_bits.md        # FastHTML patterns
│   └── notebook_best_practices.md    # nbdev/Jeremy Howard patterns
├── llm_docs/         # Extended documentation (reference when needed)
├── nbs/              # Jupyter notebooks (one per feature)
├── main.py           # FastHTML server entry point
├── mcp_server.py     # Custom MCP server for testing
└── .env              # Your API keys (create from .env.example)
```

## 🛠️ MCP Server Tools

The custom `fasthtml-tester` MCP server provides:
- `start_app` - Launch the FastHTML server
- `stop_app` - Stop the server
- `navigate_to` - Navigate to routes
- `click_element` - Click page elements
- `get_console_logs` - Capture browser console
- `get_server_logs` - View server output
- `get_app_status` - Check if app is running

## 🎯 Development Philosophy

This project follows:
- **nbdev**: Each notebook implements one feature
- **FastHTML**: Python-only web development
- **MonsterUI**: Pre-built UI components
- **Progressive Enhancement**: Build incrementally

## 📚 Documentation Strategy

- **Always in context** (via Ruler): Core patterns and project guidelines
- **Reference when needed** (`llm_docs/`): Complete API docs and advanced features

## ⚠️ Important Notes

1. **Environment Variables**: The `.env` file contains sensitive API keys. Never commit it to git.
2. **MCP Servers**: Ruler automatically configures MCP servers when you run `ruler apply`. No manual installation needed.
3. **Git Structure**: This project lives within `ai-sandbox/projects/` but has its own git repository.

## 🚦 Getting Started with Development

Ask your AI assistant to:
1. "Start the FastHTML app and navigate to the home page"
2. "Create a new notebook for the blog post data model"
3. "Implement a simple post editor interface"

The AI has full context about the project structure, conventions, and available tools through the Ruler configuration.