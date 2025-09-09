import requests
import time
import json
import os
from rich.console import Console

console = Console()

HANDLES_FILE = "handles.json"
VERIFICATION_PROBLEMS = {
    "codeforces": ("1", "A"),
}


def load_handles():
    if os.path.exists(HANDLES_FILE):
        with open(HANDLES_FILE, "r") as f:
            return json.load(f)
    return {}


def save_handle(platform, handle):
    if os.path.exists(HANDLES_FILE):
        with open(HANDLES_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data[platform] = [str(handle)]

    with open(HANDLES_FILE, "w") as f:
        json.dump(data, f, indent=4)

    console.print(f"[green]Handle for {platform} set → {handle}[/green]")


def verify(handle):
    data = load_handles()
    if handle in data.get("codeforces", []):
        console.print(f"[yellow]Codeforces handle already set: {handle}[/yellow]")
        return

    contest_id, problem_index = VERIFICATION_PROBLEMS["codeforces"]
    problem_url = f"https://codeforces.com/problemset/problem/{contest_id}/{problem_index}"
    print(f"Please submit a Compilation Error on Codeforces problem:\n   {problem_url}\n   within 60 seconds...")

    start = time.time()
    while time.time() - start < 60:
        url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=5"
        response = requests.get(url).json()
        if response["status"] != "OK":
            print("Invalid handle or Codeforces API error.")
            return
        submissions = response["result"]
        for sub in submissions:
            if str(sub["problem"].get("contestId")) == contest_id and sub["problem"].get("index") == problem_index:
                if sub.get("verdict") == "COMPILATION_ERROR":
                    sub_time = sub["creationTimeSeconds"]
                    if sub_time >= int(start):
                        print(f"Verification successful! Codeforces handle: {handle}")
                        save_handle("codeforces", handle)
                        return
        time.sleep(3)
    print("Verification failed: No compilation error submission detected in 60s.")


def set(handle):
    verify(handle)
