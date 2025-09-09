from rich.console import Console
import pyfiglet
from rich.panel import Panel
from rich.align import Align

console = Console()
def welcome():
    banner = pyfiglet.figlet_format("CPer")
    console.print(Align.center(f"[#00FFFF]{banner}[/#00FFFF]",vertical="middle"))
    console.print(Panel.fit(
        "Welcome to CPER!",
        border_style="#00FFFF"
    ),justify="center")            
    console.print("[bold #00FFFF]Your CP CLI buddy![/bold #00FFFF]",justify="center")
