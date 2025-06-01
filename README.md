# Pydantic AI Assistant with MCP Integration

A powerful command-line tool that uses Pydantic AI with Model Context Protocol (MCP) to analyze folder structures and codebases using either local Ollama models or Claude from Anthropic. Now with configurable MCP server support for enhanced capabilities.

## Features

- 🤖 **Multiple AI Providers**: Support for both Ollama (local) and Claude (Anthropic) models
- 🔌 **Configurable MCP Servers**: Choose from filesystem, GitHub, SQLite, PostgreSQL, web search, and more
- 📁 **Filesystem Access**: Direct folder analysis through MCP filesystem server
- 🗄️ **Database Integration**: Query SQLite and PostgreSQL databases
- 🔍 **Web Search**: Research capabilities with Brave Search
- 💾 **Persistent Memory**: Maintain context across conversations
- 💬 **Interactive Chat Mode**: Follow-up conversations for deeper exploration
- 🎯 **Flexible Interface**: Command-line arguments or interactive prompts
- ⚡ **Fast Analysis**: Efficient codebase understanding and documentation

## Installation

This project uses [PEP 723](https://peps.python.org/pep-0723/) script dependencies. You can run it directly with Python 3.12+:

```bash
python ai_assistant.py
```

Or install dependencies manually:

```bash
pip install pydantic-ai rich typer python-environ
```

## Quick Start

### 1. See Available MCP Servers

```bash
python ai_assistant.py --list-mcps
```

This displays all available MCP servers and their capabilities.

### 2. Interactive Mode (Recommended for first-time users)

```bash
python ai_assistant.py --interactive
```

This will guide you through:
- Selecting AI provider (Ollama or Claude)
- Choosing MCP servers to use
- Choosing folders to analyze (if needed)
- Entering your prompt
- Enabling chat mode

### 3. Command Line Mode

```bash
# Analyze with Ollama using filesystem and GitHub servers (by name)
python ai_assistant.py --provider ollama --mcp filesystem,github --folder ./src --prompt "analyze the code structure"

# Same as above using numbers (1=filesystem, 2=github)
python ai_assistant.py --provider ollama --mcp 1,2 --folder ./src --prompt "analyze the code structure"

# Use Claude with database analysis (by name)
python ai_assistant.py --provider claude --mcp filesystem,sqlite --folder ./project --prompt "analyze the database schema"

# Same using numbers (1=filesystem, 3=sqlite)
python ai_assistant.py --provider claude --mcp 1,3 --folder ./project --prompt "analyze the database schema"

# Web research with memory (by name)
python ai_assistant.py --provider claude --mcp brave-search,memory --prompt "research Python async best practices" --chat

# Same using numbers (5=brave-search, 6=memory)
python ai_assistant.py --provider claude --mcp 5,6 --prompt "research Python async best practices" --chat

# Quick chat mode with defaults (filesystem only)
python ai_assistant.py --chat
```

## Available MCP Servers

| Number | Server ID | Name | Description | Requires Folders |
|--------|-----------|------|-------------|------------------|
| 1 | `filesystem` | Filesystem | Access and analyze files and directories | Yes |
| 2 | `github` | GitHub | Interact with GitHub repositories and issues | No |
| 3 | `sqlite` | SQLite | Query and analyze SQLite databases | No |
| 4 | `postgres` | PostgreSQL | Connect to and query PostgreSQL databases | No |
| 5 | `brave-search` | Brave Search | Web search capabilities using Brave Search | No |
| 6 | `memory` | Memory | Persistent memory for conversation context | No |
| 7 | `time` | Time | Get current time and perform time-related operations | No |

You can select servers by either their ID (`filesystem`) or number (`1`) in both interactive mode and command line arguments.

## Configuration

### Environment Variables

Copy `.env.example` to `.env`

```bash
cp .env.example .env
```

Add your API keys and configuration:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://127.0.0.1:11434/
OLLAMA_MODEL=llama4

# Claude Configuration
CLAUDE_API_KEY=sk-ant-your-actual-api-key-here

# Database Configuration (if using database MCPs)
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
SQLITE_DB_PATH=/path/to/your/database.db

# Search Configuration (if using brave-search)
BRAVE_API_KEY=your-brave-search-api-key
```

### Ollama Setup

1. Install [Ollama](https://ollama.ai/)
2. Pull a model: `ollama pull llama4`
3. Ensure Ollama is running: `ollama serve`

### Claude Setup

1. Get an API key from [Anthropic Console](https://console.anthropic.com/)
2. Add it to your `.env` file as `CLAUDE_API_KEY`

## Usage Examples

### Code Analysis
```bash
python ai_assistant.py --provider claude --mcp filesystem,github --folder ./src --prompt "Explain the main architecture patterns used in this codebase and check for any related GitHub issues"

# Or using numbers:
python ai_assistant.py --provider claude --mcp 1,2 --folder ./src --prompt "Explain the main architecture patterns used in this codebase and check for any related GitHub issues"
```

### Database Analysis
```bash
python ai_assistant.py --provider claude --mcp filesystem,sqlite,postgres --folder ./migrations --prompt "Analyze the database schema and suggest optimizations"

# Or using numbers:
python ai_assistant.py --provider claude --mcp 1,3,4 --folder ./migrations --prompt "Analyze the database schema and suggest optimizations"
```

### Research with Context
```bash
python ai_assistant.py --provider claude --mcp brave-search,memory --prompt "Research current Django security best practices and remember key points for future reference" --chat

# Or using numbers:
python ai_assistant.py --provider claude --mcp 5,6 --prompt "Research current Django security best practices and remember key points for future reference" --chat
```

### Full-Stack Project Analysis
```bash
python ai_assistant.py --provider claude --mcp filesystem,github,sqlite --folder ./myproject --prompt "Provide a comprehensive analysis of this full-stack project" --chat

# Or using numbers:
python ai_assistant.py --provider claude --mcp 1,2,3 --folder ./myproject --prompt "Provide a comprehensive analysis of this full-stack project" --chat
```

### Time-Aware Analysis
```bash
python ai_assistant.py --provider claude --mcp filesystem,time --folder ./logs --prompt "Analyze recent log files from the past week"

# Or using numbers:
python ai_assistant.py --provider claude --mcp 1,7 --folder ./logs --prompt "Analyze recent log files from the past week"
```

### Multi-Database Comparison
```bash
python ai_assistant.py --provider claude --mcp sqlite,postgres,memory --prompt "Compare the schemas between our SQLite development database and PostgreSQL production database"

# Or using numbers:
python ai_assistant.py --provider claude --mcp 3,4,6 --prompt "Compare the schemas between our SQLite development database and PostgreSQL production database"
```

## Command Line Options

| Option | Short | Description |
|--------|--------|-------------|
| `--folder` | `-f` | Folder path(s) to analyze (can be used multiple times) |
| `--prompt` | `-p` | Initial prompt/question |
| `--provider` | `-m` | Model provider: `ollama` or `claude` |
| `--mcp` | | Comma-separated list of MCP servers by ID or number (e.g., `filesystem,github,time` or `1,2,7`) |
| `--follow-up`, `--chat` | `-c` | Enable conversation mode |
| `--interactive` | `-i` | Run in interactive mode |
| `--list-mcps` | | List available MCP servers and exit |

## MCP Server Combinations

### For Code Analysis
```bash
--mcp filesystem,github,memory
# Or using numbers:
--mcp 1,2,6
```
Analyze code, check GitHub issues, and maintain context.

### For Database Projects
```bash
--mcp filesystem,sqlite,postgres,time
# Or using numbers:
--mcp 1,3,4,7
```
Analyze code, query databases, and handle time-based data.

### For Research Projects
```bash
--mcp brave-search,memory,time
# Or using numbers:
--mcp 5,6,7
```
Web research with persistent memory and time awareness.

### For Full Development Workflow
```bash
--mcp filesystem,github,sqlite,memory
# Or using numbers:
--mcp 1,2,3,6
```
Complete development context with code, version control, database, and memory.

## Chat Mode

When chat mode is enabled (`--chat` or `--follow-up`), you can:

- Ask follow-up questions about the analyzed content
- Dive deeper into specific files, databases, or research topics
- Get explanations and recommendations
- Switch between different data sources seamlessly
- Type `quit`, `exit`, or `q` to end the conversation
- Use Ctrl+C to interrupt

Example chat session with multiple MCPs:
```
Initial prompt: "Analyze this Django project's database design"
Follow-up: "Search for Django performance best practices online"
Follow-up: "Check if there are any related GitHub issues in our repository"
Follow-up: "What recent changes were made to the user model?"
```

## Model Context Protocol (MCP)

This tool uses various MCP servers to provide AI models with secure, controlled access to different data sources:

### Filesystem Server
- Read file contents
- List directory structures  
- Understand project organization
- Analyze code patterns and relationships

### Database Servers (SQLite/PostgreSQL)
- Query database schemas
- Analyze table relationships
- Examine data patterns
- Suggest optimizations

### GitHub Server
- Access repository information
- Check issues and pull requests
- Analyze commit history
- Review project status

### Search Server (Brave Search)
- Research topics online
- Find current best practices
- Get up-to-date information
- Discover relevant resources

### Memory Server
- Maintain conversation context
- Remember important findings
- Build knowledge over time
- Reference previous insights

### Time Server
- Handle time-based queries
- Analyze temporal data
- Schedule-aware analysis
- Time zone conversions

## Supported File Types

The filesystem server can analyze any text-based files including:

- Source code (Python, JavaScript, TypeScript, etc.)
- Configuration files (JSON, YAML, TOML, etc.)
- Documentation (Markdown, RST, etc.)
- Build files (Makefile, justfile, etc.)
- Database files (SQLite, SQL dumps, etc.)
- And more...

## Error Handling

The tool includes comprehensive error handling for:

- Invalid API keys
- Missing directories
- Unavailable MCP servers
- Network connectivity issues
- Model availability problems
- Database connection errors

## Contributing

This project follows standard Python development practices:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Requirements

- Python 3.12+
- Node.js (for MCP servers)
- Ollama (for local models) or Claude API key
- Additional API keys for specific MCP servers (GitHub, Brave Search, etc.)

## Troubleshooting

### Common Issues

**"CLAUDE_API_KEY is missing or invalid"**
- Ensure your `.env` file contains a valid Claude API key starting with `sk-ant-`

**"Error running agent"**
- Check that Node.js is installed (required for MCP servers)
- Verify folder paths exist and are accessible
- Ensure required API keys are configured for selected MCP servers

**"Unknown MCP servers"**
- Use `--list-mcps` to see available servers
- Check spelling of server names in `--mcp` argument

**Ollama connection errors**
- Ensure Ollama is running: `ollama serve`
- Check the `OLLAMA_BASE_URL` in your `.env` file

**Database connection errors**
- Verify database credentials in `.env` file
- Ensure database servers are running and accessible
- Check database permissions

## Example Output

```
✓ Using claude model
✓ Configured MCP server: Filesystem
✓ Configured MCP server: GitHub  
✓ Configured MCP server: SQLite

Analyzing folders: ['./src']
Prompt: analyze this Django project comprehensively
MCP Servers: filesystem,github,sqlite

This Django project demonstrates a well-structured web application with the following analysis:

**Code Structure** (via Filesystem MCP):
- Clean separation of apps: users, products, orders
- Proper use of Django best practices
- Comprehensive test coverage

**GitHub Integration** (via GitHub MCP):
- 15 open issues, mostly feature requests
- Recent activity shows active development
- Good CI/CD pipeline setup

**Database Analysis** (via SQLite MCP):
- Well-normalized schema design
- Proper foreign key relationships
- Some optimization opportunities identified...

💬 Follow-up mode enabled. Type 'quit', 'exit', or press Ctrl+C to end.

Follow-up question: What are the current performance bottlenecks?

**Performance Analysis**:
Based on the codebase and database queries, I've identified several bottlenecks:
1. N+1 query problems in the product listing view
2. Missing database indexes on frequently queried fields
3. Large image uploads without optimization...

Follow-up question: Search online for Django performance optimization techniques

**Web Research Results** (via Brave Search MCP):
Current Django performance best practices include:
- Using select_related() and prefetch_related() for query optimization
- Implementing database connection pooling
- Redis caching strategies...
```