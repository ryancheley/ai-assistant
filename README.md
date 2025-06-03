# Pydantic AI Assistant with MCP Integration

A powerful command-line tool that uses Pydantic AI with Model Context Protocol (MCP) to analyze folder structures and codebases using either local Ollama models or Claude from Anthropic. Now with configurable MCP server support for enhanced capabilities.

## Features

- 🤖 **Multiple AI Providers**: Support for Ollama (local), Claude (Anthropic), and OpenAI (GPT-4) models
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

# Same using numbers (1=filesystem, 4=sqlite)
python ai_assistant.py --provider claude --mcp 1,4 --folder ./project --prompt "analyze the database schema"

# Web research with memory (by name)
python ai_assistant.py --provider claude --mcp brave-search,memory --prompt "research Python async best practices" --chat

# Same using numbers (5=brave-search, 7=memory)
python ai_assistant.py --provider claude --mcp 5,7 --prompt "research Python async best practices" --chat

# Quick chat mode with defaults (filesystem only)
python ai_assistant.py --chat
```

## Available MCP Servers

| Number | Server ID | Name | Description | Requires Folders |
|--------|-----------|------|-------------|------------------|
| 1 | `filesystem` | Filesystem | Access, analyze, read, and write files and directories | Yes |
| 2 | `github` | GitHub | Interact with GitHub repositories and issues | No |
| 3 | `azure-devops` | Azure DevOps | Interact with Azure DevOps projects, work items, repositories, and pipelines | No |
| 4 | `sqlite` | SQLite | Query and analyze SQLite databases | No |
| 5 | `brave-search` | Brave Search | Web search capabilities using Brave Search | No |
| 6 | `postgres` | PostgreSQL | Connect to and query PostgreSQL databases | No |
| 7 | `memory` | Memory | Persistent memory for conversation context | No |
| 8 | `time` | Time | Get current time and perform time-related operations | No |

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

# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here

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

### OpenAI Setup

1. Get an API key from [OpenAI Platform](https://platform.openai.com/)
2. Add it to your `.env` file as `OPENAI_API_KEY`

## Usage Examples

### Code Analysis with Azure DevOps Integration
```bash
python ai_assistant.py --provider claude --mcp filesystem,azure-devops --folder ./src --prompt "Analyze this codebase, identify performance issues, and create work items in Azure DevOps for each issue found"

# Or using numbers:
python ai_assistant.py --provider claude --mcp 1,3 --folder ./src --prompt "Analyze this codebase, identify performance issues, and create work items in Azure DevOps for each issue found"
```

### Cross-Platform DevOps Analysis
```bash
python ai_assistant.py --provider claude --mcp github,azure-devops --prompt "Compare the open issues in our GitHub repository with work items in Azure DevOps and identify any duplicates or missing items"

# Or using numbers:
python ai_assistant.py --provider claude --mcp 2,3 --prompt "Compare the open issues in our GitHub repository with work items in Azure DevOps and identify any duplicates or missing items"
```

### Project Setup and Generation
```bash
python ai_assistant.py --provider claude --mcp filesystem,azure-devops --folder ./newproject --prompt "Create a complete Python project structure and set up corresponding work items and repository in Azure DevOps"

# Or using numbers:
python ai_assistant.py --provider claude --mcp 1,3 --folder ./newproject --prompt "Create a complete Python project structure and set up corresponding work items and repository in Azure DevOps"
```

### Database Analysis with Work Item Creation
```bash
python ai_assistant.py --provider claude --mcp filesystem,sqlite,azure-devops --folder ./migrations --prompt "Analyze the current database schema and create Azure DevOps work items for required migration tasks"

# Or using numbers:
python ai_assistant.py --provider claude --mcp 1,4,3 --folder ./migrations --prompt "Analyze the current database schema and create Azure DevOps work items for required migration tasks"
```

### Research with Memory and Documentation
```bash
python ai_assistant.py --provider claude --mcp filesystem,brave-search,memory --folder ./docs --prompt "Research current Python development best practices and create comprehensive documentation" --chat

# Or using numbers:
python ai_assistant.py --provider claude --mcp 1,5,7 --folder ./docs --prompt "Research current Python development best practices and create comprehensive documentation" --chat
```

### PostgreSQL Database Analysis
```bash
python ai_assistant.py --provider claude --mcp filesystem,postgres --folder ./myproject --prompt "Analyze this Django project and optimize the PostgreSQL database queries" --chat

# Or using numbers:
python ai_assistant.py --provider claude --mcp 1,6 --folder ./myproject --prompt "Analyze this Django project and optimize the PostgreSQL database queries" --chat
```

## Command Line Options

| Option | Short | Description |
|--------|--------|-------------|
| `--folder` | `-f` | Folder path(s) to analyze (can be used multiple times) |
| `--prompt` | `-p` | Initial prompt/question |
| `--provider` | `-m` | Model provider: `ollama`, `claude`, or `openai` |
| `--mcp` | | Comma-separated list of MCP servers by ID or number (e.g., `filesystem,github,time` or `1,2,8`) |
| `--follow-up`, `--chat` | `-c` | Enable conversation mode |
| `--interactive` | `-i` | Run in interactive mode |
| `--list-mcps` | | List available MCP servers and exit |

## MCP Server Combinations

### For Azure DevOps Projects
```bash
--mcp filesystem,azure-devops,memory
# Or using numbers:
--mcp 1,3,7
```
Analyze code, manage work items, repositories, and maintain context.

### For Cross-Platform Development
```bash
--mcp filesystem,github,azure-devops
# Or using numbers:
--mcp 1,2,3
```
Complete multi-platform development with GitHub and Azure DevOps integration.

### For Database Projects
```bash
--mcp filesystem,sqlite,postgres,time
# Or using numbers:
--mcp 1,4,6,8
```
Analyze code, query databases, and handle time-based data.

### For Research Projects
```bash
--mcp brave-search,memory,time
# Or using numbers:
--mcp 5,7,8
```
Web research with knowledge graph storage, allowing creation of entities and relations from research findings, persistent memory across sessions, and time awareness.

### For Complete Development Workflow
```bash
--mcp filesystem,github,sqlite,memory
# Or using numbers:
--mcp 1,2,4,7
```
Full development context with version control, database access, and memory.

## Chat Mode

When chat mode is enabled (`--chat` or `--follow-up`), you can:

- Ask follow-up questions about the analyzed content
- Dive deeper into specific files, databases, or research topics
- Get explanations and recommendations
- Switch between different data sources seamlessly
- Type `quit`, `exit`, or `q` to end the conversation
- Use Ctrl+C to interrupt

Example chat session with Azure DevOps integration:
```
Initial prompt: "Analyze this Python project and identify areas for improvement"
Follow-up: "Create Azure DevOps work items for each performance issue found"
Follow-up: "Set up a new repository in Azure DevOps for the optimized code"
Follow-up: "Search online for Python performance best practices and update our work items with recommendations"
Follow-up: "Create comprehensive documentation in both files and Azure DevOps wiki"
```

## Model Context Protocol (MCP)

This tool uses various MCP servers to provide AI models with secure, controlled access to different data sources:

### Filesystem Server
- **Read Operations**: Read file contents, list directory structures, get file metadata, search for files
- **Write Operations**: Create new files, modify existing files, create directories, move/rename files, delete files
- **Project Generation**: Create complete project structures, boilerplate code, and configuration files
- **Code Refactoring**: Analyze and improve existing code, saving optimized versions
- **Documentation**: Generate README files, API docs, and technical documentation

### Azure DevOps Server (@tiberriver256/mcp-server-azure-devops)
- **Work Items**: Create, read, update work items, add comments, manage attachments
- **Projects**: Access project details, teams, work item types, and process templates
- **Repositories**: Browse repositories, files, commits, branches, and pull requests
- **Pipelines**: Access build and release pipelines, view runs and results
- **Users & Teams**: Manage user information, team memberships, and permissions
- **Organizations**: List and manage organization details and projects
- **Comprehensive DevOps**: Complete Azure DevOps integration for enterprise workflows

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
- Maintain conversation context through entities and relations
- Store and retrieve structured knowledge in a graph format
- Track observations about concepts, tools, and processes
- Create semantic connections between related entities
- Persist knowledge across multiple sessions
- Support fuzzy searching across entities and observations
- Enable complex knowledge graphs with typed relations
- Maintain historical context of discussions and findings

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
- Clean separation of apps and modules
- Proper use of Django best practices
- Comprehensive test coverage
- *Created optimized settings configuration*
- *Generated missing migration files*

**GitHub Integration** (via GitHub MCP):
- 15 open issues across different components
- Recent commits show active development on authentication features
- CI/CD pipeline running successfully with 92% test coverage
- *Created 3 new issues for identified security improvements*
- *Updated project board with technical debt items*

**Database Analysis** (via SQLite MCP):
- Django models properly configured
- Efficient query patterns in most views
- Some N+1 query opportunities identified
- *Generated indexes for frequently queried fields*
- *Created database optimization recommendations*...

💬 Follow-up mode enabled. Type 'quit', 'exit', or press Ctrl+C to end.

Follow-up question: What are the current performance bottlenecks?

**Performance Analysis**:
Based on the codebase and database queries, I've identified several bottlenecks:
1. N+1 query problems in the product listing view
2. Missing database indexes on frequently queried fields
3. Large file uploads without optimization...

Follow-up question: Search online for Django performance optimization techniques

**Web Research Results** (via Brave Search MCP):
Current Django performance best practices include:
- Using select_related() and prefetch_related() for query optimization
- Implementing database connection pooling
- Redis caching strategies...
```