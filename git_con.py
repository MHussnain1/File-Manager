#!/usr/bin/env python3
"""Create backdated empty Git commits for selected August 2026 dates.

Run this script from inside the Git repository whose contribution history you
intend to update. Push the resulting commits to GitHub afterward.
"""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


DATES = ("2026-08-14", "2026-08-15", "2026-08-19", "2026-08-20")


def run(*args: str, env: dict[str, str] | None = None) -> None:
    subprocess.run(args, check=True, env=env)


def main() -> None:
    try:
        run("git", "rev-parse", "--is-inside-work-tree")
    except subprocess.CalledProcessError:
        sys.exit("Error: run this script from inside an existing Git repository.")

    if subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout:
        sys.exit("Error: commit or stash your current changes before running this script.")

    for day in DATES:
        # Noon UTC avoids date shifts caused by local time zone conversions.
        timestamp = datetime.fromisoformat(f"{day}T12:00:00+00:00").isoformat()
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = timestamp
        env["GIT_COMMITTER_DATE"] = timestamp
        run("git", "commit", "--allow-empty", "-m", f"chore: contribution for {day}", env=env)
        print(f"Created commit dated {day}.")

    branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
    print(f"\nDone. Review with: git log --format=fuller -4")
    print(f"Then push with: git push origin {branch}")
    print("GitHub only counts commits that meet its contribution-graph rules.")


if __name__ == "__main__":
    main()
