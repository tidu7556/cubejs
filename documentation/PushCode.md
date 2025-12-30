# Complete Guide: Pushing Your Code Folder to Git

This guide walks you through every step of uploading your existing code to Git, from setup to completion. No prior Git experience necessary.

## What You'll Need Before Starting

Before beginning, make sure you have:
- A folder on your computer containing code you want to upload
- A GitHub account (free at github.com)
- Git installed on your computer
- Basic comfort using your computer's terminal or command prompt

## Step 1: Create a GitHub Repository (Online)

A repository is like a project folder that lives on GitHub's servers and tracks changes to your code.

### Create Your Repository

1. Go to github.com and log into your account
2. In the top-right corner, click the "+" icon, then select "New repository"
3. You'll see a form to fill out:
   - **Repository name**: Give your project a name (example: "my-first-project"). Use lowercase letters, numbers, and hyphens. No spaces.
   - **Description**: Optional but helpful. Briefly describe what your code does.
   - **Public or Private**: Choose "Public" if you want others to see it, "Private" if you want only you or specific people to access it.
4. Leave all other options at their defaults for now
5. Click "Create repository"

### You've Just Created an Empty Repository!

GitHub will show you a page with helpful information. Don't close this page yet—you'll need the URL it shows you in the next steps.

## Step 2: Prepare Your Computer (Terminal Setup)

Now you need to set up Git on your computer to talk to GitHub.

### Check If Git Is Installed

Open your terminal (Mac/Linux) or command prompt (Windows):
- **Mac**: Press Cmd+Space, type "terminal", press Enter
- **Windows**: Press Windows key, type "cmd", press Enter
- **Linux**: Open your terminal application

Type this command and press Enter:

```
git --version
```

If you see a version number (like "git version 2.40.0"), Git is installed. If you get an error, download Git from git-scm.com and follow their installer.

### Configure Git (First Time Only)

These commands tell Git who you are. Do this once on your computer:

```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Replace "Your Name" with your actual name and use the email address you used for GitHub.

## Step 3: Navigate to Your Code Folder

In your terminal, you need to navigate to the folder containing your code.

### Find Your Folder Path

First, locate where your code folder is stored on your computer. For example, it might be:
- `/Users/YourName/Documents/my-project`
- `C:\Users\YourName\Documents\my-project`
- `/home/username/my-project`

### Navigate There in Terminal

Type this command (replace the path with your actual path):

```
cd /path/to/your/code/folder
```

**Example for Mac/Linux**:
```
cd ~/Documents/my-project
```

**Example for Windows**:
```
cd C:\Users\YourName\Documents\my-project
```

After pressing Enter, your terminal should show your folder path. You're now inside your code folder.

### Verify You're in the Right Place

Type this command to see what files are in your current folder:

```
ls
```

(On Windows, use `dir` instead)

You should see your code files listed. If you don't see them, you're in the wrong folder—go back and navigate to the correct location.

## Step 4: Initialize Git in Your Folder

Initializing Git tells your folder that it's now tracked by Git.

Type this command:

```
git init
```

You'll see a message like "Initialized empty Git repository in /path/to/your/folder/.git"

This creates a hidden `.git` folder that stores all of Git's tracking information. You won't see it in your normal file browser, but it's there.

## Step 4.5: Create a .gitignore File (IMPORTANT!)

Before adding your files, you need to create a `.gitignore` file. This tells Git which files should NOT be uploaded to GitHub. This is critical for sensitive files like environment variables and secret API keys.

### Why This Matters

Some files should never be pushed to GitHub because they contain sensitive information:
- `.env` files (contain API keys, database passwords, secrets)
- `.streamlit/secrets.toml` (Streamlit configuration with sensitive data)
- Other files with credentials or personal data

If you accidentally push these, anyone who sees your GitHub repository can steal your keys and access your accounts.

### Create the .gitignore File

In your terminal (while still in your code folder), type:

```
touch .gitignore
```

(On Windows, if that doesn't work, use: `type nul > .gitignore`) or manually create.

This creates an empty `.gitignore` file.

### Open and Edit the File

Now open this file in a text editor (Notepad, VS Code, etc.) and add these lines:

```
# Environment variables
.env
.env.local
.env.*.local

# Streamlit secrets and config
.streamlit/secrets.toml

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Other
*.log
.ipynb_checkpoints/
```

Save this file as `.gitignore` in your main project folder (the same folder where you ran `git init`).

### What This Does

Each line tells Git to ignore specific files or folders:
- `.env` and `.streamlit/secrets.toml` are your most critical—these won't be uploaded
- The other entries are common files you usually don't want on GitHub (temporary files, IDE settings, etc.)

### Verify It Worked

After you add files later, you can check that sensitive files are being ignored. When you run `git status`, you should NOT see `.env` or `.streamlit/secrets.toml` listed. If you do see them, double-check your `.gitignore` file spelling.

## Step 5: Connect Your Local Folder to GitHub (After .gitignore)

Your local folder and GitHub repository need to be connected.

### Add the Remote URL

Go back to GitHub in your browser. On your repository page, look for a green "Code" button. Click it and copy the HTTPS URL (it looks like `https://github.com/yourusername/repository-name.git`).

In your terminal, type this command (replace the URL with the one you copied):

```
git remote add origin https://github.com/yourusername/repository-name.git
```

This tells your local Git folder where to send your code. "origin" is the standard name for your main GitHub repository.

### Verify the Connection

Type this command to confirm it worked:

```
git remote -v
```

You should see the URL you just added listed twice (for "fetch" and "push").

## Step 6: Add Your Files to Git

Before uploading, you need to tell Git which files you want to include.

### Stage All Your Files

Type this command to tell Git to prepare all your code files for uploading:

```
git add .
```

The period (`.`) means "add everything in this folder." Alternatively, you can add specific files:

```
git add filename.py
```

### What Does "Staging" Mean?

Staging is like putting files in a box before shipping them. You're telling Git "I want these files in my next upload."

### Check What's Staged

To see which files are ready to upload, type:

```
git status
```

You should see your files listed under "Changes to be committed" in green. If they're listed in red under "Untracked files," you need to run `git add .` again.

**Important**: Verify that `.env` and `.streamlit/secrets.toml` are NOT listed. If they appear, your `.gitignore` file isn't working correctly. Check the spelling in your `.gitignore` file.

## Step 7: Create Your First Commit

A commit is like taking a snapshot of your code at this moment. It has a message describing what changed.

### Make Your Commit

Type this command with a descriptive message:

```
git commit -m "Initial commit: Add project files"
```

The text in quotes is your commit message. Make it clear and descriptive. Examples:
- "Initial commit: Add project files"
- "Upload my Python web scraper"
- "Add blog project with HTML and CSS"

You should see output showing the files that were committed, something like:

```
[main (root-commit) abc1234] Initial commit: Add project files
 5 files changed, 234 insertions(+)
 create mode 100644 file1.py
 create mode 100644 file2.py
```

## Step 8: Upload (Push) Your Code to GitHub

Now you're ready to send everything to GitHub!

### Push Your Code

Type this command:

```
git push -u origin main
```

Breaking this down: `git push` uploads your code, `-u` sets this branch as default for future pushes, `origin` is your GitHub repository, and `main` is the main branch (like the primary version).

On your first push, you might be asked for your GitHub credentials or to authenticate. Follow the prompts. If you see something about a browser opening, that's normal—GitHub is verifying your identity.

### Success!

If everything worked, you'll see output like:

```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Writing objects: 100% (5/5), 234 bytes | 234.00 KiB/s, done.
Total 5 (delta 0), reused 0 (delta 0)
To https://github.com/yourusername/repository-name.git
 * [new branch]      main -> main
```

## Step 9: Verify on GitHub

Go back to your GitHub repository in your browser and refresh the page. You should now see your code files displayed! Your code is now on GitHub.

## What You've Accomplished

You've successfully:
1. Created a GitHub repository
2. Installed and configured Git
3. Initialized a Git repository in your local folder
4. Connected your local folder to GitHub
5. Staged your files
6. Created a commit with a descriptive message
7. Pushed your code to GitHub

## Common Issues and Solutions

### "fatal: not a git repository"

**Problem**: You're not in your code folder.

**Solution**: Make sure you've navigated to your code folder with `cd` and run `git init`.

### "fatal: Could not read from remote repository"

**Problem**: The GitHub URL is wrong or the connection failed.

**Solution**: Run `git remote -v` to check your URL. It should match exactly what's on GitHub.

### "Please tell me who you are"

**Problem**: Git doesn't know your name and email.

**Solution**: Run the configuration commands from Step 2 (the `git config` commands).

### "Permission denied (publickey)"

**Problem**: GitHub can't verify you.

**Solution**: You may need to set up SSH keys. For beginners, using HTTPS (as shown in this guide) is easier—make sure your GitHub password is correct.

## Next Steps: Making Changes and Pushing Again

After your initial push, updating your code on GitHub is simpler:

```
git add .
git commit -m "Describe what changed"
git push
```

You can repeat these three commands every time you want to upload changes. The next time, just use `git push` without the `-u origin main` part.

## Summary Commands

Here's a quick reference of all the commands you used:

```
git --version                    # Check if Git is installed
git config --global user.name "Your Name"  # Set your name
git config --global user.email "your@email.com"  # Set your email
cd /path/to/your/folder         # Navigate to your code folder
git init                         # Initialize Git in the folder
touch .gitignore                 # Create .gitignore file
git remote add origin [URL]      # Connect to GitHub
git remote -v                    # Verify the connection
git add .                        # Stage all files
git status                       # Check what's staged
git commit -m "message"          # Create a commit
git push -u origin main          # Upload to GitHub
```