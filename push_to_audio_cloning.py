#!/usr/bin/env python3
"""
Script to push changes to audio_cloning repository.
"""
import os
import subprocess
import sys

# Change to the project directory
os.chdir("/Users/dev/Documents/Text to Speech")

def run_command(cmd, capture=True):
    """Run a shell command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd, 
        capture_output=capture, 
        text=True
    )
    if result.stdout:
        print(f"STDOUT: {result.stdout}")
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    return result

# Add remote if it doesn't exist
run_command(["git", "remote", "add", "audio_clone", "https://github.com/gulkhan92/audio_cloning.git"])

# Fetch to update remote refs
run_command(["git", "fetch", "audio_clone"])

# Get current branch name
branch_result = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
current_branch = branch_result.stdout.strip()
print(f"Current branch: {current_branch}")

# Push the current branch to audio_clone repo main branch
result = run_command([
    "git", "push", "audio_clone", 
    f"{current_branch}:main", 
    "-f"
])

if result.returncode == 0:
    print("\n✅ Successfully pushed to audio_cloning repo!")
else:
    print(f"\n❌ Failed to push: {result.stderr}")
    sys.exit(1)

