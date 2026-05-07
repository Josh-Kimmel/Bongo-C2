```

 ----------------------------------------------------

   $$$$$$$\                                          
   $$  __$$\                                         
   $$ |  $$ | $$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  
   $$$$$$$\ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
   $$  __$$\ $$ /  $$ |$$ |  $$ |$$ /  $$ |$$ /  $$ |
   $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |
   $$$$$$$  |\$$$$$$  |$$ |  $$ |\$$$$$$$ |\$$$$$$  |
   \_______/  \______/ \__|  \__| \____$$ | \______/ 
                                 $$\   $$ |          
                                 \$$$$$$  |          
                                  \______/           

  Asynchronous Command and Control
 ----------------------------------------------------

```
***

## Bongo: Asynchronous Command and Control

Bongo is a lightweight, CLI, Python-based command and control server. It communicates with targets by establishing threads on a centralized [Stikked](https://github.com/claudehohl/stikked) server. This paradigm means that targets never need to communicate directly with Bongo and that commands can be issued asynchronously between Bongo and the target.

***

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running Bongo](#running-bongo)
- [CLI menu](#cli-menu)
- [Payloads and commanding](#payloads-and-commanding)
- [Project layout](#project-layout)

***

## Requirements

- **Python 3** (3.10+ recommended; the code uses `match` / `case`.)
- A running **Stikked** instance whose HTTP API is reachable from this machine. Bongo calls endpoints such as `/api/create`, `/api/paste/{id}`, and `/api/recent` (see `src/stikkedApi.py`).
- **Dependencies:** `dotenv`, `requests` (install via `requirements.txt`).

***

## Setup

1. Clone the repository and change into the project directory.
2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   ```

   - **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
   - **macOS / Linux:** `source .venv/bin/activate`

3. Install packages:

   ```bash
   pip install -r requirements.txt
   ```

***

## Configuration

### `.env` (required)

Bongo resolves the config file path from the environment variable **`serverConfigFile`**. Without it, the app exits with an error.

if `.env` is not in the project already create a `.env` file in the **project root** (same directory as `bongo.py`), for example:

```env
serverConfigFile=serverConfig.json
```

You can point `serverConfigFile` at any writable path; `serverConfig.json` in the repo root is the usual choice.

### `serverConfig.json`

Listener metadata, file posts, and server settings are stored in the JSON file named by `serverConfigFile`. This file is **gitignored** so each operator keeps local state.

- If the file is missing, invalid JSON, or missing required keys, Bongo resets it to a fresh template and prints a notice.
- **First-time initialization:** when you start Bongo and `server_data.initialized` is false, you are prompted for:
  - Full base URI to Stikked (e.g. `https://example.com` or `http://localhost` — include path prefix if Stikked is not at the site root).
  - **Username** used in Stikked API posts (`name` field in create requests).

You can re-run initialization from the CLI with menu option **0** (see below).

***

## Running Bongo

From the project root, with your virtual environment activated:

```bash
python bongo.py
```

On launch, the splash screen appears; if the server is not initialized, you are walked through Stikked URL and username. The main menu follows.

***

## CLI menu

| Option | Action |
|--------|--------|
| 0 | Initialize server (Stikked URL, username) |
| 1 | View settings |
| 2 | View listeners |
| 3 | View files |
| 4 | Create listener (new paste on Stikked) |
| 5 | Post file (upload file contents as a paste) |
| 6 | Send commands (reply to a listener paste) |
| 7 | Delete sessions (placeholder) |
| 8 | View command queue (listener paste and replies) |
| 9 | Generate payload |
| 10 | Exit |

***

## Payloads and commanding

To put an implant on a machine that talks back through Stikked:

1. **Create a listener** — Use menu option **4** (*Create listener*). That registers a paste on Stikked and stores its ID in your config. You need that **listener paste ID** for the next step.
2. **Generate a payload** — Use option **9** (*Generate payload*). Enter the listener ID (and any other prompts, such as poll interval). Bongo writes the generated script under **`extras/Payloads/`** (that folder is gitignored).
3. **Run on the target** — Copy the generated file to the system you want to control and execute it there (Python, PowerShell, or Bash, depending on what you generated).

To issue tasks, use option **6** (*Send commands*). Pick the same listener by ID. **Each line** you enter is treated as **one shell command** (blank line ends input). Bongo posts that text as a **reply** to the listener paste on Stikked. The payload **polls** Stikked every **N seconds** (the interval you set when generating it), looks for reply pastes titled like `RE: <listener name>`, and runs the body of each new reply. **Each reply paste is only executed once** (the implant remembers reply IDs it has already run). When you send commands, you can set an **expiration in minutes** so the command paste drops off Stikked after that time (**self-destruct** on the server side); the implant still runs it the first time it sees it, after at most one poll interval.

***

## Project layout

Main entry point is **`bongo.py`**; implementation lives under **`src/`**. Example client logic is under **`extras/Templates/`**; generated implants land in **`extras/Payloads/`**.

Gitignored by default: `serverConfig.json`, `.env`, and `extras/Payloads/*`.

***
