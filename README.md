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

```bash
# Clone the repository
git clone https://github.com/12ahmedashraf/CPer.git
cd CPer

# Install Python dependencies
pip install -r requirements.txt pyfiglet rich requests

# Run directly with Python
python main.py
```

> **Tip:** If you want a single executable, you can build your own binary with PyInstaller:
>
> ```bash
> pyinstaller --onefile --clean main.py -n cper
> # On Windows, the EXE will be in dist\cper.exe
> # On Linux/macOS, the executable will be in dist/cper
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

# Or from source
python main.py
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

## License

Licensed under **MIT License**. See [LICENSE](LICENSE) for details.
