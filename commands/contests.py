import requests
from datetime import datetime, timezone
from rich.console import Console
from rich.table import Table

console = Console()

def contests(count=5):
    url = "https://codeforces.com/api/contest.list"
    try:
        resp = requests.get(url, params={"gym": False}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "OK":
            console.print("[red]Error fetching contest list from Codeforces[/red]")
            return
    except Exception as e:
        console.print(f"[red]Exception while fetching contests:[/red] {e}")
        return

    all_contests = data["result"]
    upcoming = [c for c in all_contests if c.get("phase") == "BEFORE"]
    upcoming.sort(key=lambda c: c.get("startTimeSeconds", 0))

    if not upcoming:
        console.print("[yellow]No upcoming contests found.[/yellow]")
        return

    table = Table(title=" Upcoming Codeforces Contests ")
    table.add_column("Date & Time (UTC)", style="cyan")
    table.add_column("Contest Name", style="magenta")
    table.add_column("Duration", style="green")
    table.add_column("Link", style="blue")

    for contest in upcoming[:count]:
        name = contest.get("name", "N/A")
        secs = contest.get("startTimeSeconds")
        dt = datetime.fromtimestamp(secs, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC") if secs else "N/A"
        duration = contest.get("durationSeconds", 0)
        hrs, rem = divmod(duration, 3600)
        mins = rem // 60
        dur_str = f"{hrs}h {mins}m"
        link = f"https://codeforces.com/contests/{contest.get('id')}"

        table.add_row(dt, name, dur_str, link)

    console.print(table)
