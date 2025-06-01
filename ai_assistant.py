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
from typing import Optional
from enum import Enum

from pathlib import Path
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.openai import OpenAIProvider
from rich import print
from rich.console import Console
from rich.prompt import Prompt, Confirm
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

async def _main(*, folders: list[Path], prompt: str, provider: ModelProvider, follow_up: bool = False):
    args = []
    for folder in folders:
        if folder.is_dir():
            args.append(str(folder))
        else:
            console.print(f"[yellow]Warning: {folder} is not a valid directory and will be skipped[/yellow]")

    if not args:
        console.print("[red]Error: No valid directories provided[/red]")
        return

    try:
        model = get_model(provider)
        console.print(f"[green]✓ Using {provider.value} model[/green]")
    except Exception as e:
        console.print(f"[red]Failed to initialize {provider.value} model: {e}[/red]")
        return

    agent = Agent(
        model=model,
        mcp_servers=[
            MCPServerStdio(
                "npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                ]
                + args,
            ),
        ],
    )

    try:
        async with agent.run_mcp_servers():
            # Initial question
            result = await agent.run(prompt)
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
                        result = await agent.run(follow_up_prompt)
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
    follow_up: bool = typer.Option(False, "--follow-up", "--chat", "-c", help="Enable follow-up questions after initial response"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Run in interactive mode"),
):
    """
    Analyze folders using Pydantic AI with MCP filesystem server.
    
    Use --interactive flag to enter paths and prompt interactively,
    or provide them via command line arguments.
    
    Use --follow-up or --chat to enable a conversation mode where you can ask follow-up questions.
    
    Examples:
        python ai_assistant.py --provider ollama
        python ai_assistant.py --provider claude --folder ./src --prompt "analyze the code" --follow-up
        python ai_assistant.py --interactive --chat
        python ai_assistant.py --chat  # Quick chat mode with defaults
    """
    
    # If interactive mode or no arguments provided, get input interactively
    if interactive or (not folders and not prompt and not provider):
        console.print("[bold green]🤖 Pydantic AI Folder Analyzer[/bold green]\n")
        
        if not provider:
            provider = get_model_provider()
            
        if not folders:
            folders = get_folders()
            
        if not folders:
            console.print("[red]No folders provided. Exiting.[/red]")
            raise typer.Exit(1)
            
        if not prompt:
            prompt = get_prompt()
            
        if not follow_up:
            follow_up = Confirm.ask("Enable follow-up questions?", default=True)
    
    # Use defaults if still not provided
    if not folders:
        folders = [Path("/Users/ryan/Documents/testbed/pydantic-wip")]
        
    if not prompt:
        prompt = "which justfile recipes do we have?"
        
    if not provider:
        provider = ModelProvider.OLLAMA
    
    console.print(f"\n[bold]Analyzing folders:[/bold] {[str(f) for f in folders]}")
    console.print(f"[bold]Prompt:[/bold] {prompt}")
    console.print(f"[bold]Provider:[/bold] {provider.value}")
    if follow_up:
        console.print(f"[bold]Follow-up mode:[/bold] enabled")
    console.print()
    
    asyncio.run(_main(folders=folders, prompt=prompt, provider=provider, follow_up=follow_up))

if __name__ == "__main__":
    typer.run(main)