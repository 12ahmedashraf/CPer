from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from commands.helpp import help
from commands.welcome import welcome
from commands.set import set
from commands.stats import stats
from commands.suggest import suggest
from rich.console import Console
from commands.contests import contests
console = Console()

COMMANDS = {
    "help": help,
    "set": set,
    "stats": stats,
    "suggest": suggest,
    "contests": lambda: contests(5),
}

completer = WordCompleter(list(COMMANDS.keys()) + ["exit"], ignore_case=True)

def cper():
    try:
        welcome()
        help()
    except Exception:
        console.print("Warning! can't run CPer pls try again!")
        console.print_exception()

    session = PromptSession()
    while True:
        try:
            cmd = session.prompt("cper> ", completer=completer).strip()
            if not cmd:
                continue

            parts = cmd.split()
            command = parts[0]
            args = parts[1:]

            if command == "exit":
                console.print("[green]Goodbye![/green]")
                break
            elif command in COMMANDS:
                if command == "set":
                    if len(args) == 0:
                        console.print("[red]Error:[/red] Missing arguments. Usage: set <handle>")
                    else:
                        COMMANDS[command](args[0])
                elif command == "stats":
                    if len(args) < 1:
                        COMMANDS[command]()
                    else:
                        COMMANDS[command](args[0])
                elif command == "contests":
                    COMMANDS[command]()
                elif command == "suggest":
                    rating_range = None
                    topics = []

                    if args:
                        if "-" in args[0]:  
                            try:
                                lo, hi = args[0].split("-")
                                rating_range = (int(lo), int(hi))
                                topics = args[1:]
                            except:
                                console.print("[red]Invalid rating range format. Use like 1400-1600[/red]")
                        else:
                            topics = args
                    COMMANDS[command](rating_range, topics)
                else:
                    COMMANDS[command](*args)
            else:
                console.print(f"[red]Unknown command:[/red] {command}. Type 'help' for available commands.")

        except KeyboardInterrupt:
            continue
        except EOFError:
            break
