#!/usr/bin/env python3
"""
Export learning records and push to remote Git repository.

This script helps automate the workflow of:
1. Checking/initializing git repository
2. Organizing exported content
3. Committing changes
4. Pushing to remote
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
import shutil


def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if check and result.returncode != 0:
            print(f"Error running command: {cmd}")
            if result.stderr:
                print(f"stderr: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"Exception running command: {e}")
        return None


def init_git_repo(repo_path):
    """Initialize git repository if not exists."""
    git_dir = Path(repo_path) / ".git"
    
    if not git_dir.exists():
        print(f"Initializing git repository at {repo_path}...")
        result = run_command("git init", cwd=repo_path, check=False)
        return result is not None
    else:
        print(f"Git repository already exists at {repo_path}")
        return False


def setup_remote(repo_path, remote_url):
    """Configure git remote."""
    # Check if remote already exists
    remotes = run_command("git remote", cwd=repo_path, check=False)
    
    if remotes and "origin" in remotes:
        print("Remote 'origin' already exists. Updating URL...")
        run_command(f"git remote set-url origin {remote_url}", cwd=repo_path)
    else:
        print(f"Adding remote 'origin': {remote_url}")
        run_command(f"git remote add origin {remote_url}", cwd=repo_path)


def create_readme(repo_path):
    """Create README.md if not exists."""
    readme_path = Path(repo_path) / "README.md"
    
    if not readme_path.exists():
        print("Creating README.md...")
        content = """# Learning Records

Repository for storing learning notes and knowledge summaries.

## Structure

- `subjects/` - Organized by subject/topic
- `daily/` - Organized by date

## Usage

Record daily learning content in Markdown format.
"""
        readme_path.write_text(content, encoding='utf-8')
        return True
    return False


def create_gitignore(repo_path):
    """Create .gitignore if not exists."""
    gitignore_path = Path(repo_path) / ".gitignore"
    
    if not gitignore_path.exists():
        print("Creating .gitignore...")
        content = """# Temporary files
*.tmp
*.temp
.DS_Store
Thumbs.db

# Editor files
.vscode/
.idea/
*.swp
*.swo

# Private/Sensitive
*.key
*.secret
.env
"""
        gitignore_path.write_text(content, encoding='utf-8')
        return True
    return False


def organize_file(src_file, repo_path, category="subjects"):
    """Move exported file to organized location."""
    src = Path(src_file)
    if not src.exists():
        print(f"Source file not found: {src_file}")
        return None
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = src.name
    
    # Create directory structure
    dest_dir = Path(repo_path) / category
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # If filename doesn't start with date, prepend it
    if not filename.startswith(date_str):
        dest_filename = f"{date_str}-{filename}"
    else:
        dest_filename = filename
    
    dest = dest_dir / dest_filename
    
    # Copy file
    shutil.copy2(src, dest)
    print(f"Copied to: {dest}")
    
    return dest


def commit_and_push(repo_path, message=None, branch="main"):
    """Stage, commit and push changes."""
    # Check if there are changes
    status = run_command("git status --porcelain", cwd=repo_path, check=False)
    
    if not status:
        print("No changes to commit.")
        return True
    
    # Stage all changes
    print("Staging changes...")
    run_command("git add .", cwd=repo_path)
    
    # Commit
    if not message:
        date_str = datetime.now().strftime("%Y-%m-%d")
        message = f"Add learning records - {date_str}"
    
    print(f"Committing: {message}")
    run_command(f'git commit -m "{message}"', cwd=repo_path)
    
    # Push
    print(f"Pushing to origin/{branch}...")
    result = run_command(f"git push -u origin {branch}", cwd=repo_path, check=False)
    
    if result is not None:
        print("[OK] Successfully pushed to remote!")
        return True
    else:
        print("[ERROR] Push failed. Please check your remote configuration.")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Export learning records and push to Git remote"
    )
    parser.add_argument(
        "--repo-path",
        default=os.path.expanduser("~/learning-records"),
        help="Path to learning records repository (default: ~/learning-records)"
    )
    parser.add_argument(
        "--remote-url",
        help="Remote repository URL (e.g., https://github.com/user/repo.git)"
    )
    parser.add_argument(
        "--source-file",
        help="Path to the exported file to organize"
    )
    parser.add_argument(
        "--category",
        default="subjects",
        help="Category folder (default: subjects)"
    )
    parser.add_argument(
        "--message", "-m",
        help="Commit message"
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Git branch (default: main)"
    )
    parser.add_argument(
        "--init-only",
        action="store_true",
        help="Only initialize the repository, don't commit/push"
    )
    
    args = parser.parse_args()
    
    # Ensure repo path exists
    repo_path = Path(args.repo_path)
    repo_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize git repo
    is_new = init_git_repo(repo_path)
    
    # Create basic files
    create_readme(repo_path)
    create_gitignore(repo_path)
    
    # Setup remote if provided
    if args.remote_url:
        setup_remote(repo_path, args.remote_url)
    
    # Organize source file if provided
    if args.source_file:
        organize_file(args.source_file, repo_path, args.category)
    
    # Commit and push (unless init-only)
    if not args.init_only:
        if is_new and not args.remote_url:
            print("\n[!] Repository initialized but no remote configured.")
            print("Add remote with: git remote add origin <url>")
            return
        
        commit_and_push(repo_path, args.message, args.branch)
    
    print(f"\n[OK] Learning records repository: {repo_path}")


if __name__ == "__main__":
    main()
