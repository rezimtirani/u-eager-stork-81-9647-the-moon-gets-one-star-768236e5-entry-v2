"""Upload main.py + README.md for the corrected Moon entry to GitHub.

Creates or updates each file through the GitHub Contents API, so the
same script works for a first upload and for a re-upload. The parent
uploads the remaining files (LICENSE, this script, entry-state.json)
with a companion script so the bundle tree matches the GitHub tree.
"""

import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request  # noqa: E402

OWNER = "rezimtirani"
REPO = "u-eager-stork-81-9647-the-moon-gets-one-star-768236e5-entry-v2"
API = "https://api.github.com"
ENTRY = Path(
    "/home/hatch/workspace/makefun"
    "/u-eager-stork-81-9647-the-moon-gets-one-star-768236e5-entry-v2"
)
FILES = ["main.py", "README.md"]


def github_request(method, url, payload=None):
    body = None
    headers = {"Accept": "application/vnd.github+json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    add_surrogate_to_request(request, "custom.github", allowed_hosts=["api.github.com"])
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def lookup_sha(path):
    try:
        info = github_request("GET", f"{API}/repos/{OWNER}/{REPO}/contents/{path}")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    return info.get("sha")


def push_file(path):
    local = ENTRY / path
    encoded = base64.b64encode(local.read_bytes()).decode("ascii")
    payload = {
        "message": f"Add {path} — Moon Gets One Star (corrected, 114 chars)",
        "content": encoded,
    }
    sha = lookup_sha(path)
    if sha is not None:
        payload["sha"] = sha
    result = github_request(
        "PUT", f"{API}/repos/{OWNER}/{REPO}/contents/{path}", payload
    )
    print(f"{path}: {result['commit']['sha']}")
    return result["commit"]["sha"]


def main():
    for name in FILES:
        push_file(name)
    print(f"Done: {OWNER}/{REPO}")


if __name__ == "__main__":
    main()
