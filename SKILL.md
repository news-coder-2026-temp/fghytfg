---
name: export-learning-records
description: Export conversation learning records to a Git repository and push to remote. Use when the user wants to (1) export/save learning content from the current conversation, (2) create or update a learning records repository, (3) push learning records to a remote Git repository like GitHub/GitLab, or (4) backup conversation content to version control.
---

# Export Learning Records

This skill exports the current conversation's learning content to a Git repository and pushes it to a remote server.

## Workflow

### 1. Check/Create Repository

First, check if a learning records repository already exists. If not, create one:

```bash
# Check if git repo exists in the target directory
cd <learning-records-path>
git status

# If not a git repo, initialize it
git init
```

### 2. Export Conversation Content

Use Kimi's `/export` command to export the conversation:

- Export format: Markdown (recommended for learning records)
- Export destination: Save to the learning records repository directory

### 3. Organize Files

Organize the exported content with proper structure:

```
learning-records/
├── README.md                 # Overview of learning records
├── subjects/                 # Organize by subject/topic
│   ├── <subject-name>/
│   │   └── <date>-<topic>.md
├── daily/                    # Or organize by date
│   └── <YYYY-MM-DD>-<topic>.md
└── .gitignore
```

### 4. Git Operations

Stage, commit, and push the changes:

```bash
# Add files
git add .

# Commit with descriptive message
git commit -m "Add learning records: <brief description>"

# Configure remote if not exists
git remote add origin <remote-url>

# Push to remote
git push -u origin <branch-name>
```

## Common Patterns

### First-time Setup

For new learning records repository:

1. Create directory: `mkdir -p ~/learning-records`
2. Initialize git: `cd ~/learning-records && git init`
3. Create README: Describe the purpose and structure
4. Create .gitignore: Ignore sensitive or temporary files
5. First commit: `git add . && git commit -m "Initial commit"`
6. Add remote: `git remote add origin <your-remote-url>`
7. Push: `git push -u origin main`

### Daily Export Routine

1. Export conversation to the appropriate directory
2. Review and organize content
3. Stage changes: `git add <files>`
4. Commit: `git commit -m "<date>: <topic learned>"`
5. Push: `git push`

### Remote Repository Options

- **GitHub**: `git remote add origin https://github.com/<username>/<repo>.git`
- **GitLab**: `git remote add origin https://gitlab.com/<username>/<repo>.git`
- **Gitee**: `git remote add origin https://gitee.com/<username>/<repo>.git`

## Best Practices

1. **Commit Messages**: Use descriptive messages like "2024-01-15: Learned Python decorators"
2. **File Naming**: Use `<date>-<topic>.md` format for easy sorting
3. **Organization**: Group by subject or date based on preference
4. **Regular Commits**: Don't let changes accumulate; commit regularly
5. **Private Repos**: Consider making the repository private if content is personal
