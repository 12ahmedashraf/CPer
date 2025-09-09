import json
import requests
import random
from rich.console import Console

console = Console()

def cf_color(rating):
    if rating is None:
        return "white"
    if rating < 1200: return "bright_white"
    if rating < 1400: return "green"
    if rating < 1600: return "cyan"
    if rating < 1900: return "blue"
    if rating < 2100: return "magenta"
    if rating < 2400: return "yellow"
    if rating < 3000: return "red"
    return "bright_red"

def load_handles():
    try:
        with open("handles.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"codeforces": []}

def get_user_rating_and_solved(handle):
    """Fetch user rating and solved problems from Codeforces API"""
    user_rating = None
    solved = set()
    try:
        resp = requests.get(f"https://codeforces.com/api/user.info?handles={handle}", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data["status"] == "OK":
            user_rating = data["result"][0].get("rating")
    except Exception:
        pass
    try:
        resp = requests.get(f"https://codeforces.com/api/user.status?handle={handle}", timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data["status"] == "OK":
            for sub in data["result"]:
                if sub.get("verdict") == "OK" and "problem" in sub:
                    prob = sub["problem"]
                    key = f"{prob.get('contestId','')}/{prob.get('index','')}"
                    solved.add(key)
    except Exception:
        pass

    return user_rating, solved

def suggest(rating_range=None, topics=None):
    handles = load_handles()
    cf_handles = handles.get("codeforces", [])

    user_rating, solved = None, set()
    if cf_handles:
        user_rating, solved = get_user_rating_and_solved(cf_handles[0])

    try:
        resp = requests.get("https://codeforces.com/api/problemset.problems", timeout=20)
        resp.raise_for_status()
        data = resp.json()
        if data["status"] != "OK":
            console.print("[red]Failed to fetch problems from Codeforces![/red]")
            return
    except Exception:
        console.print("[red]Error fetching problems![/red]")
        return

    problems = data["result"]["problems"]

    min_rating, max_rating = None, None
    if rating_range:
        min_rating, max_rating = rating_range

    filtered = []
    for prob in problems:
        rating = prob.get("rating")
        if rating is None or rating % 100 != 0:
            continue

        key = f"{prob.get('contestId','')}/{prob.get('index','')}"
        if key in solved:
            continue

        if min_rating is not None and rating < min_rating:
            continue
        if max_rating is not None and rating > max_rating:
            continue

        if topics:
            tags = prob.get("tags", [])
            if not any(topic.lower() in [t.lower() for t in tags] for topic in topics):
                continue

        filtered.append(prob)

    if rating_range is None and not topics:
        if user_rating:
            nearest = round(user_rating / 100) * 100
            target_ratings = [nearest + 100, nearest + 200]
            filtered = [p for p in problems
                        if p.get("rating") in target_ratings
                        and f"{p.get('contestId','')}/{p.get('index','')}" not in solved]
        else:
            filtered = [p for p in problems
                        if p.get("rating") and 1000 <= p.get("rating") <= 1700
                        and f"{p.get('contestId','')}/{p.get('index','')}" not in solved]

    if not filtered:
        console.print("[yellow]No unsolved problems found with the given filters![/yellow]")
        return

    selected_problem = random.choice(filtered)
    rating = selected_problem.get("rating", None)

    console.print("[green]Suggested problem:[/green]")
    console.print(f"- {selected_problem['name']} ", end="")
    console.print(f"(Rating: {rating if rating else 'N/A'})", style=cf_color(rating))

    if topics:
        console.print(f"  Tags: {', '.join(selected_problem.get('tags', []))}")
    console.print(f"  URL: https://codeforces.com/problemset/problem/{selected_problem.get('contestId','')}/{selected_problem.get('index','')}")
