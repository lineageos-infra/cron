import os
import sys

USERNAME=os.environ.get("GERRIT_USERNAME")
PASSWORD=os.environ.get("GERRIT_PASSWORD")
URL=os.environ.get("GERRIT_URL", "https://review.lineageos.org")

if not USERNAME or not PASSWORD:
    print("GERRIT_USERNAME or GERRIT_PASSWORD not provided")
    sys.exit(1)
