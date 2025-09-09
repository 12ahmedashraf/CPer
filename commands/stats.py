import requests
import json
from collections import Counter
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

def load_handles():
    try:
        with open("handles.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"codeforces": []}

def cf_color(rating):
    if rating is None:
        return "white"
    if rating < 1200: return "bright_white"
    if rating < 1400: return "green"
    if rating < 1600: return "cyan"
    if rating < 1900: return "dark_blue"
    if rating < 2100: return "purple"
    if rating < 2400: return "yellow"
    if rating < 3000: return "red"
    return "bright_red"

def stats_codeforces(handle):
    try:
        user_info = requests.get(f"https://codeforces.com/api/user.info?handles={handle}").json()
        if user_info["status"] != "OK":
            console.print(f"[red]Error fetching user info for {handle} try again later![/red]")
            return
        user = user_info["result"][0]

        contest_data = requests.get(f"https://codeforces.com/api/user.rating?handle={handle}").json()
        contests = contest_data["result"] if contest_data["status"] == "OK" else []

        submissions_data = requests.get(f"https://codeforces.com/api/user.status?handle={handle}").json()
        submissions = submissions_data["result"] if submissions_data["status"] == "OK" else []

        console.print("\n[bold underline]Codeforces Profile[/bold underline]")
        rating = user.get("rating")
        max_rating = user.get("maxRating")
        color = cf_color(rating)
        color2 = cf_color(max_rating)

        console.print(f"Handle: [bold {color}]{user['handle']}[/bold {color}]")
        console.print(f"Rank: [bold {color}]{user.get('rank','-')}[/bold {color}]")
        console.print(f"Rating: [bold {color}]{rating if rating else 'Unrated'}[/bold {color}]")
        console.print(f"Max Rating: [bold {color2}]{max_rating if max_rating else '-'}[/bold {color2}]")
        console.print(f"Friends of: {user.get('friendOfCount','-')}")
        console.print()

        if contests:
            table = Table(title="Recent Contests", box=box.MINIMAL_DOUBLE_HEAD)
            table.add_column("Contest", style="cyan", overflow="fold")
            table.add_column("Rank", style="green")
            table.add_column("Rating", justify="right")
            for c in contests[-10:]:
                contest_name = c["contestName"]
                rank = str(c["rank"])
                new_rating = str(c["newRating"])
                table.add_row(contest_name, rank, f"[{cf_color(c['newRating'])}]{new_rating}[/{cf_color(c['newRating'])}]")
            console.print(table)
            ranks = [c["rank"] for c in contests]
            avg_rank = sum(ranks) / len(ranks)
            best_rank = min(ranks)
            worst_rank = max(ranks)

            console.print("\n[bold underline]Contest Stats[/bold underline]")
            console.print(f"Total Contests: [cyan]{len(contests)}[/cyan]")
            console.print(f"Best Rank: [green]{best_rank}[/green] | Worst Rank: [red]{worst_rank}[/red] | Average Rank: [yellow]{avg_rank:.1f}[/yellow]")

            categories = Counter()
            for c in contests:
                name = c["contestName"]
                if "Div. 1" in name: categories["Div. 1"] += 1
                elif "Div. 2" in name: categories["Div. 2"] += 1
                elif "Div. 3" in name: categories["Div. 3"] += 1
                elif "Div. 4" in name: categories["Div. 4"] += 1
                elif "Educational" in name: categories["Educational"] += 1
                elif "Global" in name: categories["Global"] += 1
                else: categories["Other"] += 1

            if categories:
                table = Table(title="Contests by Category", box=box.MINIMAL_DOUBLE_HEAD)
                table.add_column("Category", style="yellow")
                table.add_column("Count", style="green")
                for cat, cnt in categories.items():
                    table.add_row(cat, str(cnt))
                console.print(table)
        solved = set()
        unsolved = set()
        by_rating = Counter()
        by_tag = Counter()
        solved_days = set()

        today = datetime.utcnow().date()
        solved_week, solved_month, solved_year = set(), set(), set()

        for sub in submissions:
            contest_id = sub["problem"].get("contestId", "NA")
            index = sub["problem"].get("index", "NA")
            pid = (contest_id, index)
            tags = sub["problem"].get("tags", [])
            rating_p = sub["problem"].get("rating")
            when = datetime.utcfromtimestamp(sub["creationTimeSeconds"]).date()

            if sub["verdict"] == "OK":
                solved.add(pid)
                solved_days.add(when)
                if (today - when).days < 7: solved_week.add(pid)
                if when.month == today.month and when.year == today.year: solved_month.add(pid)
                if when.year == today.year: solved_year.add(pid)
                if rating_p: by_rating[rating_p] += 1
                for t in tags: by_tag[t] += 1
            else:
                if pid not in solved:
                    unsolved.add(pid)

        console.print("\n[bold underline]Problem Stats[/bold underline]")
        console.print(f"Solved: [green]{len(solved)}[/green]")
        console.print(f"Unsolved: [red]{len(unsolved)}[/red]")
        console.print(f"This week: [cyan]{len(solved_week)}[/cyan] | This month: [cyan]{len(solved_month)}[/cyan] | This year: [cyan]{len(solved_year)}[/cyan]")

        if by_rating:
            table = Table(title="Solved by Rating", box=box.MINIMAL_DOUBLE_HEAD)
            table.add_column("Rating", style="cyan")
            table.add_column("Count", style="green")
            for r in sorted(by_rating):
                table.add_row(str(r), f"[{cf_color(r)}]{by_rating[r]}[/{cf_color(r)}]")
            console.print(table)

        if by_tag:
            table = Table(title="Solved by Topic", box=box.MINIMAL_DOUBLE_HEAD)
            table.add_column("Tag", style="cyan")
            table.add_column("Count", style="green")
            for tag, cnt in by_tag.most_common(10):
                table.add_row(tag, str(cnt))
            console.print(table)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def stats(handle=None):
    if not handle:
        handles = load_handles()
        cf_handles = handles.get("codeforces", [])
        if cf_handles:
            handle = cf_handles[0]
        else:
            console.print("[red]No handle is set or provided. Please provide one![/red]")
            return
    stats_codeforces(handle)
