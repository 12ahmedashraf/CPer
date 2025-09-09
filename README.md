# cper

[![Build and Release](https://github.com/12ahmedashraf/CPer/actions/workflows/release.yml/badge.svg)](https://github.com/12ahmedashraf/CPer/actions)

`cper` is a **terminal program** designed for **competitive programmers** to:

- Improve your competitive programming skills
- Track your progress
- Train effectively on **Codeforces**

**Track. Practice. Dominate!**

---

## Features

- Cross-platform binaries (**Windows**, **Linux**, **macOS**)
- Save and manage your Codeforces handle
- Detailed stats (rating, contests, solved problems by rating/tag, etc.)
- Problem suggestion with rating and topic filters
- Upcoming contest listings
- Rich-colored output for a clean experience

---

## Installation

1. Go to the **[Releases](https://github.com/<your-username>/<your-repo>/releases)** page.
2. Download the latest binary for your OS:
   - `cper-windows.exe` (Windows)
   - `cper-linux` (Linux)
   - `cper-macos` (macOS)
3. (Optional) Move the binary into a directory on your `PATH`.

> **Linux/macOS**: you may need to make the binary executable:
>
> ```bash
> chmod +x ./cper-linux
> # or
> chmod +x ./cper-macos
> ```

---

## Usage

Run directly:

```bash
# Linux
./cper-linux

# macOS
./cper-macos

# Windows
cper-windows.exe
```

If you moved it to your `PATH`, you can run simply:

```bash
cper
```

---

## Commands

### Available Commands:

| Command                                      | Description                                                                                              |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `set <handle>`                               | Link your Codeforces handle to **cper**                                                                  |
| `stats <handle>`                             | Show stats of a handle (defaults to your linked handle)                                                  |
| `suggest --rating_range <x-y> --topic <tag>` | Suggest problems (filters optional). Without filters, suggests problems near your rating (+100 or +200). |
| `contests`                                   | List upcoming Codeforces contests                                                                        |
| `help`                                       | Show the help page                                                                                       |
| `exit`                                       | Quit `cper`                                                                                              |

---

## Build From Source (Optional)

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

pip install -r requirements.txt pyinstaller
pyinstaller --onefile main.py -n cper
```

---

## License

Licensed under **MIT License**. See [LICENSE](LICENSE) for details.
