import argparse
import json
import logging
import sys
import importlib.metadata
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme
from rich.logging import RichHandler

from botsmith.app import BotSmithApp
from botsmith.core.plugin import PluginManager

# --- Rich Setup ---
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
})
console = Console(theme=custom_theme)

def setup_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )

def create_bot(args):
    """Handle `botsmith create` command."""
    app = BotSmithApp()
    
    user_request = args.prompt
    project_name = args.name or "unnamed_project"

    console.print(Panel(f"[bold blue]Creating bot:[/bold blue] {project_name}\n[bold blue]Request:[/bold blue] {user_request}", title="BotSmith"))

    try:
        result = app.create_bot(user_request, project_name)
    except Exception as e:
        console.print(f"[error]Failed to create bot: {e}[/error]")
        if args.debug:
            console.print_exception()
        return

    # Show summary
    res_data = result.get("result", {})
    status = res_data.get("status", "unknown")
    
    if status == "success":
        console.print(f"[success]Bot created successfully![/success]")
        context = res_data.get("context", {})
        generated = []
        if "generated_files" in context:
            generated = context["generated_files"]
        elif "files" in res_data:
            generated = res_data["files"]

        table = Table(title="Generated Files")
        table.add_column("File", style="cyan")
        table.add_column("Path", style="dim")

        for f in generated:
            if isinstance(f, dict):
                table.add_row(f.get('filename', 'unknown'), str(f.get('path', '')))
            elif isinstance(f, str):
                table.add_row(Path(f).name, f)
        
        console.print(table)
    else:
        console.print("[error]Bot creation failed![/error]")
        console.print(f"Error: {res_data.get('error')}")

    if args.save_workflow:
        out = Path("workflow_output.json")
        out.write_text(json.dumps(result.get("workflow", {}), indent=2))
        console.print(f"[dim]Workflow saved to {out.resolve()}[/dim]")

def list_projects(args):
    """Show generated projects."""
    root = Path("botsmith/generated")

    if not root.exists():
        console.print("[warning]No generated projects found.[/warning]")
        return

    table = Table(title="Generated Projects")
    table.add_column("Name", style="green")
    table.add_column("Path", style="dim")

    for p in root.iterdir():
        if p.is_dir():
            table.add_row(p.name, str(p.resolve()))
    
    console.print(table)

def init_project(args):
    """Scaffold a project without AI."""
    from botsmith.tools.filesystem import FileSystemTool
    from botsmith.agents.specialized.project_scaffold_agent import ProjectScaffoldAgent
    
    name = args.name.strip().lower().replace(" ", "_")
    console.print(f"[info]Initializing project: {name}[/info]")
    
    # Use current working directory
    fs = FileSystemTool(sandbox_dir=Path(".")) 
    agent = ProjectScaffoldAgent(None, None) # No LLM needed
    
    try:
        # Execute scaffold task
        result = agent.execute("scaffold_project", {
            "filesystem": fs,
            "project_name": name
        })
        
        if result.get("scaffolded"):
            console.print(f"[success]Project '{name}' initialized![/success]")
            console.print(f"Files created: {len(result.get('files', []))}")
        
    except Exception as e:
         console.print(f"[error]Init failed: {e}[/error]")

def version(args):
    try:
        ver = importlib.metadata.version("botsmith")
    except importlib.metadata.PackageNotFoundError:
        ver = "dev"
    console.print(f"BotSmith CLI v{ver}")

def main():
    parser = argparse.ArgumentParser(
        prog="botsmith",
        description="BotSmith Command-Line Interface"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    sub = parser.add_subparsers(dest="command")

    # create
    create_p = sub.add_parser("create", help="Generate a new bot from a prompt")
    create_p.add_argument("prompt", type=str, help="Natural language bot request")
    create_p.add_argument("--name", type=str, help="Project name")
    create_p.add_argument("--save-workflow", action="store_true", help="Save workflow JSON")
    create_p.set_defaults(func=create_bot)

    # list
    list_p = sub.add_parser("list", help="List generated projects")
    list_p.set_defaults(func=list_projects)
    
    # init
    init_p = sub.add_parser("init", help="Initialize a blank project (scaffold only)")
    init_p.add_argument("name", type=str, help="Project name")
    init_p.set_defaults(func=init_project)

    # version
    ver_p = sub.add_parser("version", help="Show CLI version")
    ver_p.set_defaults(func=version)

    # Parse
    args = parser.parse_args()
    
    setup_logging(args.debug)
    
    # Load Plugins
    pm = PluginManager()
    pm.load_plugins()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)

if __name__ == "__main__":
    main()
