#!/usr/bin/env python3
"""
ToolBreakdown Publisher
Run by Hermes cron: generates articles, commits, pushes to deploy.
"""

import subprocess
import sys
import os

PROJECT_ROOT = os.path.expanduser("~/projects/toolbreakdown")

def run(cmd, cwd=PROJECT_ROOT):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

print("=== ToolBreakdown Publisher ===")

# 1. Pull latest
out, err, rc = run("git pull origin main")
print(f"[pull] {out}")

# 2. Scan for new keywords (weekly) — skip if queue has pending items
# 3. Generate next batch of articles (keep index.astro files)
# Note: content-engine.py generates into src/pages/{type}/, preserving existing files
out, err, rc = run("python3 content-engine.py --limit 5")
print(f"[generate]\n{out}")
if rc != 0:
    print(f"ERROR: {err}")
    sys.exit(1)

# 4. Build site to verify
out, err, rc = run("npm run build")
print(f"[build] exit={rc}")
if rc != 0:
    print(f"BUILD ERROR:\n{err}")
    sys.exit(1)

# 5. Count pages built
import glob
pages = glob.glob(os.path.join(PROJECT_ROOT, "dist/**/*.html"), recursive=True)
print(f"[build] {len(pages)} pages generated")

# 6. Git commit and push main
out, err, rc = run("git add src/pages/ data/ && git status --short")
if out:
    out2, err2, rc2 = run(f'git commit -m "auto: generate {len(out.splitlines())} articles" && git push origin main')
    print(f"[push main] {out2}")
    
    # 7. Deploy to GitHub Pages (gh-pages branch)
    out3, err3, rc3 = run("npx --yes gh-pages -d dist -m 'auto deploy'")
    print(f"[deploy] {out3}")
else:
    print("[push] No changes to commit")

print("=== Done ===")
