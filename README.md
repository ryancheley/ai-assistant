# Pydantic AI Folder Analyzer

A powerful command-line tool that uses Pydantic AI with Model Context Protocol (MCP) to analyze folder structures and codebases using either local Ollama models or Claude from Anthropic.

## Features

- 🤖 **Multiple AI Providers**: Support for both Ollama (local) and Claude (Anthropic) models
- 📁 **Filesystem Access**: Direct folder analysis through MCP filesystem server
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

### 1. Interactive Mode (Recommended for first-time users)

```bash
python ai_assistant.py --interactive
```

This will guide you through:
- Selecting AI provider (Ollama or Claude)
- Choosing folders to analyze
- Entering your prompt
- Enabling chat mode

### 2. Command Line Mode

```bash
# Analyze with Ollama (local)
python ai_assistant.py --provider ollama --folder ./src --prompt "analyze the code structure"

# Analyze with Claude and enable chat
python ai_assistant.py --provider claude --folder ./myproject --prompt "what are the main components?" --chat

# Quick chat mode with defaults
python ai_assistant.py --chat
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env`

```
cp .env.example .env
```
Add your Claude API Key (if you want to use Claude)

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
python ai_assistant.py --provider claude --folder ./src --prompt "Explain the main architecture patterns used in this codebase"
```

### Documentation Generation
```bash
python ai_assistant.py --provider ollama --folder ./api --prompt "Generate API documentation for the endpoints in this folder" --chat
```

### Code Review
```bash
python ai_assistant.py --provider claude --folder ./feature-branch --prompt "Review this code for potential issues and improvements"
```

### Project Understanding
```bash
python ai_assistant.py --interactive
# Then enter multiple folders and ask: "What does this project do and how is it structured?"
```

## Command Line Options

| Option | Short | Description |
|--------|--------|-------------|
| `--folder` | `-f` | Folder path(s) to analyze (can be used multiple times) |
| `--prompt` | `-p` | Initial prompt/question |
| `--provider` | `-m` | Model provider: `ollama` or `claude` |
| `--follow-up`, `--chat` | `-c` | Enable conversation mode |
| `--interactive` | `-i` | Run in interactive mode |

## Chat Mode

When chat mode is enabled (`--chat` or `--follow-up`), you can:

- Ask follow-up questions about the analyzed folders
- Dive deeper into specific files or patterns
- Get explanations and recommendations
- Type `quit`, `exit`, or `q` to end the conversation
- Use Ctrl+C to interrupt

Example chat session:
```
Initial prompt: "What are the main components of this Django project?"
Follow-up: "How is user authentication handled?"
Follow-up: "Show me the database models"
Follow-up: "Are there any security concerns I should address?"
```

## Model Context Protocol (MCP)

This tool uses the [@modelcontextprotocol/server-filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) MCP server to provide AI models with secure, controlled access to your filesystem. The AI can:

- Read file contents
- List directory structures  
- Understand project organization
- Analyze code patterns and relationships

## Supported File Types

The filesystem server can analyze any text-based files including:

- Source code (Python, JavaScript, TypeScript, etc.)
- Configuration files (JSON, YAML, TOML, etc.)
- Documentation (Markdown, RST, etc.)
- Build files (Makefile, justfile, etc.)
- And more...

## Error Handling

The tool includes comprehensive error handling for:

- Invalid API keys
- Missing directories
- Network connectivity issues
- Model availability problems

## Contributing

This project follows standard Python development practices:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Requirements

- Python 3.12+
- Node.js (for MCP filesystem server)
- Ollama (for local models) or Claude API key

## Troubleshooting

### Common Issues

**"CLAUDE_API_KEY is missing or invalid"**
- Ensure your `.env` file contains a valid Claude API key starting with `sk-ant-`

**"Error running agent"**
- Check that Node.js is installed (required for MCP server)
- Verify folder paths exist and are accessible

**Ollama connection errors**
- Ensure Ollama is running: `ollama serve`
- Check the `OLLAMA_BASE_URL` in your `.env` file

## Example Output

```
✓ Using claude model

Analyzing folders: ['./src']
Prompt: analyze the code structure

This codebase appears to be a well-structured Python application with the following key components:

1. **Main Module** (`ai_assistant.py`): CLI tool using Typer for command-line interface
2. **Model Integration**: Support for both Ollama and Anthropic Claude models
3. **MCP Integration**: Uses Model Context Protocol for filesystem access
4. **Configuration**: Environment-based configuration with .env support

The architecture follows clean separation of concerns with clear provider abstraction...

💬 Follow-up mode enabled. Type 'quit', 'exit', or press Ctrl+C to end.

Follow-up question: How could I extend this to support more AI providers?
```