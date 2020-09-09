import os
import sys

USERNAME=os.environ.get("GERRIT_USERNAME")
PASSWORD=os.environ.get("GERRIT_PASSWORD")
URL=os.environ.get("GERRIT_URL", "https://review.lineageos.org/")

SLACK_WEBHOOK=os.environ.get("SLACK_WEBHOOK")
SLACK_ICON="https://avatars1.githubusercontent.com/u/44036562?s=280&v=4"

if not USERNAME or not PASSWORD:
    print("GERRIT_USERNAME or GERRIT_PASSWORD not provided")
    sys.exit(1)
