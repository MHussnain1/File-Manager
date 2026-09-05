#!/usr/bin/env python3
"""Create dated empty Git commits for September 1, 2, 3, and 4.

Run this script from inside an existing Git repository. It creates commits only;
push the branch afterwards if you want the commits to appear on a hosting site.
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime


DAYS = (1, 2, 3, 4)


def run_git(arguments, env=None):
    return subprocess.run(["git", *arguments], env=env, text=True, check=False)


def main():
    parser = argparse.ArgumentParser(
        description="Create one empty commit on each of September 1–4."
    )
    parser.add_argument(
        "--year",
        type=int,
        default=datetime.now().year,
        help="Year to use (default: current year).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the commits that would be made without changing Git history.",
    )
    args = parser.parse_args()

    if run_git(["rev-parse", "--is-inside-work-tree"]).returncode != 0:
        sys.exit("Error: run this script from inside a Git repository.")

    for day in DAYS:
        # ISO 8601 with a fixed time keeps author and committer dates identical.
        commit_date = f"{args.year}-09-{day:02d}T12:00:00"
        message = f"chore: contribution for September {day}, {args.year}"

        if args.dry_run:
            print(f"Would create: {commit_date} — {message}")
            continue

        environment = os.environ.copy()
        environment["GIT_AUTHOR_DATE"] = commit_date
        environment["GIT_COMMITTER_DATE"] = commit_date
        result = run_git(["commit", "--allow-empty", "-m", message], env=environment)
        if result.returncode != 0:
            sys.exit(f"Error: stopped before September {day}.")
        print(f"Created commit dated {commit_date}")

    if not args.dry_run:
        print("Done. Push your current branch with: git push")


if __name__ == "__main__":
    main()
