#!/usr/bin/env python3
"""Two-way sync between local native/ and Overleaf via git.

Mirrors the pattern used by 02_quench_paper/overleaf_sync.py.

Usage:
  python3 overleaf_sync.py pull
  python3 overleaf_sync.py push
"""
import subprocess, os, shutil, sys
from pathlib import Path

PROJECT_ID = "6a0a232fc5f8b090a582317a"
TOKEN = "olp_2aPpgxthfG39mCVWfzLqLF3kAknwrr4iDCi4"
REPO_URL = f"https://git:{TOKEN}@git.overleaf.com/{PROJECT_ID}"
LOCAL_DIR = Path(__file__).parent
CLONE_DIR = Path("/tmp/overleaf_native_sync")

ENV = os.environ.copy()
ENV["GIT_TERMINAL_PROMPT"] = "0"

# Files to keep in sync (sources + .bbl so Overleaf's bibliography renders
# even when its auto-bibtex pass doesn't fire on the first Recompile)
SYNC_FILES = ["main.tex", "references.bib", "main.bbl"]
SYNC_DIRS  = []  # add e.g. "figures" once we have any


def ensure_clone():
    if (CLONE_DIR / ".git").exists():
        return
    if CLONE_DIR.exists():
        shutil.rmtree(CLONE_DIR)
    subprocess.run(["git", "clone", REPO_URL, str(CLONE_DIR)],
                   check=True, env=ENV, capture_output=True)
    print("Cloned Overleaf project.")


def pull():
    ensure_clone()
    os.chdir(CLONE_DIR)
    subprocess.run(["git", "pull", "--rebase"], check=True, env=ENV, capture_output=True)
    for f in SYNC_FILES:
        src = CLONE_DIR / f
        if src.exists():
            shutil.copy2(src, LOCAL_DIR / f)
            print(f"  pulled {f} -> local")
    for d in SYNC_DIRS:
        src = CLONE_DIR / d
        dst = LOCAL_DIR / d
        if src.exists():
            dst.mkdir(exist_ok=True)
            for f in src.iterdir():
                if f.is_file():
                    shutil.copy2(f, dst / f.name)
            print(f"  pulled {d}/ -> local")


def push():
    ensure_clone()
    os.chdir(CLONE_DIR)
    subprocess.run(["git", "pull", "--rebase"], check=True, env=ENV, capture_output=True)
    print("Pulled latest from Overleaf.")

    for f in SYNC_FILES:
        src = LOCAL_DIR / f
        if src.exists():
            shutil.copy2(src, CLONE_DIR / f)

    for d in SYNC_DIRS:
        src = LOCAL_DIR / d
        dst = CLONE_DIR / d
        if src.exists():
            dst.mkdir(exist_ok=True)
            for f in src.glob("*"):
                if f.is_file():
                    shutil.copy2(f, dst / f.name)

    subprocess.run(["git", "add", "-A"], check=True, env=ENV)
    result = subprocess.run(["git", "status", "--porcelain"],
                            capture_output=True, text=True, env=ENV)
    if not result.stdout.strip():
        print("No changes to push.")
        return

    msg = sys.argv[2] if len(sys.argv) > 2 else "native: local update"
    subprocess.run(["git", "commit", "-m", msg], check=True, env=ENV, capture_output=True)
    subprocess.run(["git", "push"], check=True, env=ENV, capture_output=True)
    print(f"Pushed: {msg}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("pull", "push"):
        print(__doc__)
        sys.exit(1)
    {"pull": pull, "push": push}[sys.argv[1]]()
