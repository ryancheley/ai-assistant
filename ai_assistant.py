# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pydantic-ai",
#     "rich",
#     "typer",
#     "python-environ",
# ]
# ///
import asyncio
import os
import typer
from typing import Optional, List
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from pathlib import Path
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.openai import OpenAIProvider
from rich import print
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
import environ

console = Console()

# Initialize environment variables
env = environ.Env(
    OLLAMA_BASE_URL=(str, 'http://127.0.0.1:11434/'),
    OLLAMA_MODEL=(str, 'llama4'),
    CLAUDE_API_KEY=(str, ''),
)

# Read .env file if it exists
env_file = Path('.env')
if env_file.exists():
    environ.Env.read_env(str(env_file))

class ModelProvider(str, Enum):
    OLLAMA = "ollama"
    CLAUDE = "claude"

@dataclass
class Message:
    """Represents a message in the conversation history"""
    role: str  # 'user' or 'assistant'
    content: str

@dataclass
class MessageHistory:
    """Manages conversation history"""
    messages: List[Message] = None
    
    def __init__(self):
        self.messages = []
    
    def add_message(self, role: str, content: str):
        self.messages.append(Message(role=role, content=content))
    
    def get_context(self) -> str:
        """Returns formatted conversation history"""
        if not self.messages:
            return ""
        
        context = "Previous conversation:\n"
        for msg in self.messages:
            context += f"{msg.role}: {msg.content}\n"
        return context

@dataclass
class MCPServer:
    """Configuration for an MCP server"""
    name: str
    description: str
    command: str
    args: List[str]
    requires_folders: bool = False
    
    def get_server_config(self, folder_args: List[str] = None) -> MCPServerStdio:
        """Get the MCPServerStdio configuration for this server"""
        args = self.args.copy()
        if self.requires_folders and folder_args:
            args.extend(folder_args)
        
        return MCPServerStdio(self.command, args=args)

# Available MCP servers
AVAILABLE_MCP_SERVERS = {
    "filesystem": MCPServer(
        name="Filesystem",
        description="Access, analyze, read, and write files and directories",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
        requires_folders=True
    ),
    "github": MCPServer(
        name="GitHub",
        description="Interact with GitHub repositories and issues",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"]
    ),
    "azure-devops": MCPServer(
        name="Azure DevOps",
        description="Interact with Azure DevOps projects, work items, repositories, and pipelines",
        command="npx",
        args=["-y", "@tiberriver256/mcp-server-azure-devops"]
    ),
    "sqlite": MCPServer(
        name="SQLite",
        description="Query and analyze SQLite databases",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-sqlite"]
    ),
    "brave-search": MCPServer(
        name="Brave Search",
        description="Web search capabilities using Brave Search",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-brave-search"]
    ),
    "postgres": MCPServer(
        name="PostgreSQL",
        description="Connect to and query PostgreSQL databases",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-postgres"]
    ),
    "memory": MCPServer(
        name="Memory",
        description="Persistent memory for conversation context",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-memory"]
    ),
    "time": MCPServer(
        name="Time",
        description="Get current time and perform time-related operations",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-time"]
    ),
}

def get_model(provider: ModelProvider):
    """Get the appropriate model based on provider selection"""
    
    if provider == ModelProvider.OLLAMA:
        base_url = env('OLLAMA_BASE_URL')
        if not base_url.endswith('/v1'):
            base_url = base_url.rstrip('/') + '/v1'
            
        return OpenAIModel(
            model_name=env('OLLAMA_MODEL'),
            provider=OpenAIProvider(base_url=base_url),
        )
    
    elif provider == ModelProvider.CLAUDE:
        api_key = env('CLAUDE_API_KEY')
        
        if not api_key or api_key.startswith('sk...'):
            console.print("[red]❌ Error: CLAUDE_API_KEY is missing or invalid in your .env file[/red]")
            console.print("[yellow]Please add a valid Claude API key to your .env file:[/yellow]")
            console.print("CLAUDE_API_KEY=sk-ant-your-actual-api-key-here")
            raise typer.Exit(1)
        
        # Validate API key format
        if not api_key.startswith('sk-ant-'):
            console.print(f"[red]❌ Error: API key doesn't start with 'sk-ant-'[/red]")
            console.print("[yellow]Claude API keys should start with 'sk-ant-'[/yellow]")
            raise typer.Exit(1)
        
        # Set the API key as an environment variable for AnthropicModel
        os.environ['ANTHROPIC_API_KEY'] = api_key
            
        return AnthropicModel(
            model_name='claude-3-5-sonnet-20241022',
        )
    
    else:
        raise ValueError(f"Unsupported model provider: {provider}")

def display_mcp_servers():
    """Display available MCP servers in a nice table"""
    table = Table(title="Available MCP Servers")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Requires Folders", style="yellow")
    
    for server_id, server in AVAILABLE_MCP_SERVERS.items():
        table.add_row(
            server_id,
            server.name,
            server.description,
            "Yes" if server.requires_folders else "No"
        )
    
    console.print(table)

def get_selected_mcp_servers(default_servers: List[str] = None) -> List[str]:
    """Interactively get MCP server selections from the user using numbered choices"""
    if default_servers is None:
        default_servers = ["filesystem"]
    
    console.print("\n[bold blue]Select MCP servers to use:[/bold blue]")
    
    # Create numbered list of servers
    server_list = list(AVAILABLE_MCP_SERVERS.items())
    
    table = Table(title="Available MCP Servers")
    table.add_column("Number", style="cyan", no_wrap=True)
    table.add_column("ID", style="yellow", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Requires Folders", style="red")
    
    for i, (server_id, server) in enumerate(server_list, 1):
        table.add_row(
            str(i),
            server_id,
            server.name,
            server.description,
            "Yes" if server.requires_folders else "No"
        )
    
    console.print(table)
    
    # Show default selection
    default_numbers = []
    for default_server in default_servers:
        for i, (server_id, _) in enumerate(server_list, 1):
            if server_id == default_server:
                default_numbers.append(str(i))
                break
    
    console.print(f"\n[yellow]Default selection: {', '.join(default_numbers)} ({', '.join(default_servers)})[/yellow]")
    console.print("[cyan]Enter server numbers separated by commas, or press Enter for defaults:[/cyan]")
    console.print("[dim]Example: 1,2,7 (for filesystem, github, and time)[/dim]")
    
    selection = Prompt.ask("Server numbers", default=",".join(default_numbers))
    
    # Parse number selections
    try:
        selected_numbers = [int(s.strip()) for s in selection.split(",") if s.strip()]
    except ValueError:
        console.print("[red]Invalid input. Please enter numbers separated by commas.[/red]")
        return default_servers
    
    # Validate and convert numbers to server IDs
    valid_servers = []
    for num in selected_numbers:
        if 1 <= num <= len(server_list):
            server_id = server_list[num - 1][0]
            server = AVAILABLE_MCP_SERVERS[server_id]
            valid_servers.append(server_id)
            console.print(f"[green]✓ Added {num}: {server.name}[/green]")
        else:
            console.print(f"[red]✗ Invalid number: {num} (valid range: 1-{len(server_list)})[/red]")
    
    if not valid_servers:
        console.print("[yellow]No valid servers selected, using defaults[/yellow]")
        return default_servers
    
    return valid_servers

async def _main(*, folders: list[Path], prompt: str, provider: ModelProvider, 
               mcp_servers: List[str], follow_up: bool = False):
    # Initialize message history
    message_history = MessageHistory()
    args = []
    for folder in folders:
        if folder.is_dir():
            args.append(str(folder))
        else:
            console.print(f"[yellow]Warning: {folder} is not a valid directory and will be skipped[/yellow]")

    # Check if we need folders but don't have any valid ones
    folder_required_servers = [s for s in mcp_servers if AVAILABLE_MCP_SERVERS[s].requires_folders]
    if folder_required_servers and not args:
        console.print(f"[red]Error: The following MCP servers require folders: {', '.join(folder_required_servers)}[/red]")
        console.print("[red]Please provide valid directories or remove these servers from your selection[/red]")
        return

    try:
        model = get_model(provider)
        console.print(f"[green]✓ Using {provider.value} model[/green]")
    except Exception as e:
        console.print(f"[red]Failed to initialize {provider.value} model: {e}[/red]")
        return

    # Build MCP server configurations
    mcp_server_configs = []
    for server_id in mcp_servers:
        if server_id in AVAILABLE_MCP_SERVERS:
            server = AVAILABLE_MCP_SERVERS[server_id]
            try:
                config = server.get_server_config(args if server.requires_folders else None)
                mcp_server_configs.append(config)
                console.print(f"[green]✓ Configured MCP server: {server.name}[/green]")
            except Exception as e:
                console.print(f"[red]Failed to configure {server.name}: {e}[/red]")

    if not mcp_server_configs:
        console.print("[red]Error: No MCP servers could be configured[/red]")
        return

    agent = Agent(
        model=model,
        mcp_servers=mcp_server_configs,
    )

    try:
        async with agent.run_mcp_servers():
            # Initial question
            # Add context from message history if available
            context = message_history.get_context()
            full_prompt = f"{context}\n{prompt}" if context else prompt
            
            # Run the agent
            result = await agent.run(full_prompt)
            
            # Add to message history
            message_history.add_message('user', prompt)
            message_history.add_message('assistant', result.output)
            print(f"{result.output}\n")
            print(result.usage())
            
            # Follow-up conversation loop
            if follow_up:
                console.print("\n[bold blue]💬 Follow-up mode enabled. Type 'quit', 'exit', or press Ctrl+C to end.[/bold blue]")
                
                while True:
                    try:
                        follow_up_prompt = Prompt.ask("\n[bold green]Follow-up question", default="")
                        
                        if not follow_up_prompt.strip():
                            continue
                            
                        if follow_up_prompt.lower() in ['quit', 'exit', 'q']:
                            console.print("[yellow]Ending conversation.[/yellow]")
                            break
                            
                        # Continue the conversation with the same agent
                        # Include conversation history in follow-up
                        context = message_history.get_context()
                        full_prompt = f"{context}\n{follow_up_prompt}"
                        
                        # Run the agent
                        result = await agent.run(full_prompt)
                        
                        # Add to message history
                        message_history.add_message('user', follow_up_prompt)
                        message_history.add_message('assistant', result.output)
                        print(f"\n{result.output}\n")
                        print(result.usage())
                        
                    except KeyboardInterrupt:
                        console.print("\n[yellow]Conversation ended by user.[/yellow]")
                        break
                    except Exception as e:
                        console.print(f"[red]Error in follow-up: {e}[/red]")
                        continue

    except Exception as e:
        console.print(f"[red]Error running agent: {e}[/red]")

def get_folders() -> list[Path]:
    """Interactively get folder paths from the user"""
    folders = []
    console.print("[bold blue]Enter folder paths to analyze (press Enter on empty line to finish):[/bold blue]")
    console.print("[dim]Note: Some MCP servers (like filesystem) require folder paths[/dim]")
    
    while True:
        path_input = Prompt.ask("Folder path", default="")
        
        if not path_input.strip():
            break
            
        path = Path(path_input.strip())
        if path.exists() and path.is_dir():
            folders.append(path)
            console.print(f"[green]✓ Added: {path}[/green]")
        else:
            console.print(f"[red]✗ Invalid directory: {path}[/red]")
            
    return folders

def get_prompt() -> str:
    """Interactively get the prompt from the user"""
    console.print("\n[bold blue]Enter your prompt:[/bold blue]")
    return Prompt.ask("Prompt", default="which justfile recipes do we have?")

def get_model_provider() -> ModelProvider:
    """Interactively get the model provider from the user"""
    console.print("\n[bold blue]Select model provider:[/bold blue]")
    console.print("1. Ollama (local)")
    console.print("2. Claude (Anthropic)")
    
    choice = Prompt.ask("Choose provider", choices=["1", "2"], default="1")
    
    if choice == "1":
        return ModelProvider.OLLAMA
    else:
        return ModelProvider.CLAUDE

def main(
    folders: Optional[list[Path]] = typer.Option(None, "--folder", "-f", help="Folder paths to analyze"),
    prompt: Optional[str] = typer.Option(None, "--prompt", "-p", help="Prompt to run against the agent"),
    provider: Optional[ModelProvider] = typer.Option(None, "--provider", "-m", help="Model provider to use"),
    mcp_servers: Optional[str] = typer.Option(None, "--mcp", help="Comma-separated list of MCP servers to use by ID or number (e.g., 'filesystem,github,time' or '1,2,7')"),
    follow_up: bool = typer.Option(False, "--follow-up", "--chat", "-c", help="Enable follow-up questions after initial response"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Run in interactive mode"),
    list_mcps: bool = typer.Option(False, "--list-mcps", help="List available MCP servers and exit"),
):
    """
    Analyze folders using Pydantic AI with configurable MCP servers.
    
    Use --interactive flag to enter paths and prompt interactively,
    or provide them via command line arguments.
    
    Use --follow-up or --chat to enable a conversation mode where you can ask follow-up questions.
    
    Use --list-mcps to see all available MCP servers.
    
    Examples:
        python ai_assistant.py --list-mcps
        python ai_assistant.py --provider claude --mcp filesystem,github
        python ai_assistant.py --provider claude --mcp 1,2 --folder ./src --prompt "analyze the code" --follow-up
        python ai_assistant.py --interactive --chat
        python ai_assistant.py --chat  # Quick chat mode with defaults
    """
    
    # List MCPs and exit if requested
    if list_mcps:
        console.print("[bold green]🔌 Available MCP Servers[/bold green]\n")
        
        server_list = list(AVAILABLE_MCP_SERVERS.items())
        table = Table(title="Available MCP Servers")
        table.add_column("Number", style="cyan", no_wrap=True)
        table.add_column("ID", style="yellow", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Requires Folders", style="red")
        
        for i, (server_id, server) in enumerate(server_list, 1):
            table.add_row(
                str(i),
                server_id,
                server.name,
                server.description,
                "Yes" if server.requires_folders else "No"
            )
        
        console.print(table)
        console.print("\n[cyan]Use --mcp with server IDs or numbers, e.g.:[/cyan]")
        console.print("  --mcp filesystem,github,time")
        console.print("  --mcp 1,2,7")
        raise typer.Exit(0)
    
    # Parse MCP servers from command line
    selected_mcp_servers = None
    if mcp_servers:
        server_ids = [s.strip() for s in mcp_servers.split(",") if s.strip()]
        selected_mcp_servers = []
        server_list = list(AVAILABLE_MCP_SERVERS.keys())
        
        for server_spec in server_ids:
            # Check if it's a number
            if server_spec.isdigit():
                server_num = int(server_spec)
                if 1 <= server_num <= len(server_list):
                    selected_mcp_servers.append(server_list[server_num - 1])
                else:
                    console.print(f"[red]Error: Server number {server_num} is out of range (1-{len(server_list)})[/red]")
                    console.print("[yellow]Use --list-mcps to see available servers[/yellow]")
                    raise typer.Exit(1)
            # Check if it's a server ID
            elif server_spec in AVAILABLE_MCP_SERVERS:
                selected_mcp_servers.append(server_spec)
            else:
                console.print(f"[red]Error: Unknown MCP server: {server_spec}[/red]")
                console.print("[yellow]Use --list-mcps to see available servers[/yellow]")
                raise typer.Exit(1)
    
    # If interactive mode or no arguments provided, get input interactively
    if interactive or (not folders and not prompt and not provider and not selected_mcp_servers):
        console.print("[bold green]🤖 Pydantic AI Folder Analyzer[/bold green]\n")
        
        if not provider:
            provider = get_model_provider()
            
        if not selected_mcp_servers:
            selected_mcp_servers = get_selected_mcp_servers()
        
        # Check if we need folders for any selected servers
        folder_required = any(AVAILABLE_MCP_SERVERS[s].requires_folders for s in selected_mcp_servers)
        
        if not folders and folder_required:
            folders = get_folders()
            
        if not prompt:
            prompt = get_prompt()
            
        if not follow_up:
            follow_up = Confirm.ask("Enable follow-up questions?", default=True)
    
    # Use defaults if still not provided
    if not folders:
        # Only set default folder if we have MCP servers that need it
        if selected_mcp_servers and any(AVAILABLE_MCP_SERVERS[s].requires_folders for s in selected_mcp_servers):
            folders = [Path("/Users/ryan/Documents/testbed/pydantic-wip")]
        else:
            folders = []
        
    if not prompt:
        prompt = "which justfile recipes do we have?"
        
    if not provider:
        provider = ModelProvider.OLLAMA
    
    if not selected_mcp_servers:
        selected_mcp_servers = ["filesystem"]
    
    console.print(f"\n[bold]Analyzing folders:[/bold] {[str(f) for f in folders] if folders else 'None'}")
    console.print(f"[bold]Prompt:[/bold] {prompt}")
    console.print(f"[bold]Provider:[/bold] {provider.value}")
    console.print(f"[bold]MCP Servers:[/bold] {', '.join(selected_mcp_servers)}")
    if follow_up:
        console.print(f"[bold]Follow-up mode:[/bold] enabled")
    console.print()
    
    asyncio.run(_main(
        folders=folders, 
        prompt=prompt, 
        provider=provider, 
        mcp_servers=selected_mcp_servers,
        follow_up=follow_up
    ))

if __name__ == "__main__":
    typer.run(main)