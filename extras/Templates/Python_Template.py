import html
import subprocess
import time
import requests

STIKKED_BASE = input("Stikked server URL (e.g. http://localhost): ").strip().rstrip("/")
LISTENER_ID  = input("Listener paste ID: ").strip()
POLL_INTERVAL = int(input("Poll interval in seconds: ").strip())

def get_url(path):
    return STIKKED_BASE + "/" + path.lstrip("/")

def get_listener_name():
    resp = requests.get(get_url("/api/paste/" + LISTENER_ID))
    resp.raise_for_status()
    return resp.json().get("title", "")

def get_reply_ids(listener_name):
    resp = requests.get(get_url("/api/recent"))
    resp.raise_for_status()
    expected_title = "RE: " + listener_name
    return [p["pid"] for p in resp.json() if p.get("title") == expected_title]

def get_paste_raw(pid):
    resp = requests.get(get_url("/api/paste/" + pid))
    resp.raise_for_status()
    return html.unescape(resp.json().get("raw", ""))

def run_commands(raw_text):
    for line in raw_text.splitlines():
        line = line.strip()
        if line:
            subprocess.run(line, shell=True)

listener_name = get_listener_name()
seen_pids = set()

while True:
    try:
        for pid in get_reply_ids(listener_name):
            if pid not in seen_pids:
                seen_pids.add(pid)
                run_commands(get_paste_raw(pid))
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(POLL_INTERVAL)
