from rich.console import Console
import pyfiglet
from rich.panel import Panel
from rich.table import Table

console = Console()

def help():
    console.print("\n[bold cyan]Usage:[/bold cyan]")
    console.print("  [white]cper is a terminal program designed for competitive programmers to help them improve their competitive \n  programming skills , track their progress and train on codeforces !.[command] [options][/white]\n")
    console.print("[bold cyan]Commands:[/bold cyan]")
    table = Table(show_header=False, show_lines=False, expand=False,padding=(0,2))
    table.add_row("[bold yellow] set <handle>[/bold yellow]", "---> link your codeforces handle to CPer!")
    table.add_row("[bold yellow] stats <handle>[/bold yellow]", "---> Show the statistics of the user with this handle (shows your stats if you don't provide one)")
    table.add_row("[bold yellow] suggest --rating_range <x-y> --topic <tag>[/bold yellow]", "---> suggest problems to solve with rating & topics filters,if no filters provided it suggests problems with your rating +100 or +200")
    table.add_row("[bold yellow] contests[/bold yellow]", "---> List upcoming codeforces contests")
    table.add_row("[bold yellow] help[/bold yellow]", "---> show the help page")
    table.add_row("[bold yellow] exit[/bold yellow]", "---> exit cper")
    console.print(table)
    console.print("[bold #00FFFF]Track. Practice. Dominate![/bold #00FFFF]",justify="center")