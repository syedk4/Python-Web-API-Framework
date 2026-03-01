# GitHub Repository Setup Guide

This guide will help you create a GitHub repository and push your HTTPie-Python-Web project to it.

## Prerequisites

- Git installed on your system
- GitHub account created
- Terminal/Command Prompt access

## Step-by-Step Instructions

### Option 1: Using GitHub Web Interface (Recommended for Beginners)

#### Step 1: Create Repository on GitHub

1. Go to [GitHub](https://github.com) and log in
2. Click the **"+"** icon in the top-right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name:** `HTTPie-Python-Web`
   - **Description:** "A web-based API testing framework built with Flask"
   - **Visibility:** Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**
6. **Keep this page open** - you'll need the repository URL

#### Step 2: Initialize Git and Push Code

Open PowerShell or Command Prompt and run these commands:

```powershell
# Navigate to your project directory
cd C:\Users\slatheef\Documents\HTTPie\HTTPie-Python-Web

# Initialize git repository
git init

# Add all files (respecting .gitignore)
git add .

# Check what files will be committed (verify config.env is NOT listed)
git status

# Create initial commit
git commit -m "Initial commit: HTTPie-Python-Web API testing framework"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/HTTPie-Python-Web.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Important:** Replace `YOUR_USERNAME` with your actual GitHub username in the remote URL!

---

### Option 2: Using GitHub CLI (Advanced)

If you have GitHub CLI installed:

```powershell
# Navigate to project directory
cd C:\Users\slatheef\Documents\HTTPie\HTTPie-Python-Web

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Python-API-Testing-Framework"

# Create GitHub repository and push (will prompt for authentication)
gh repo create Python-API-Testing-Framework --public --source=. --remote=origin --push
```

---

## Verification Steps

### Before Pushing - Verify Sensitive Files Are Excluded

Run this command to see what files will be committed:

```powershell
git status
```

**Verify that these files/folders are NOT listed:**
- ❌ `config.env` (contains API keys)
- ❌ `__pycache__/` directories
- ❌ `test-results/` contents (except .gitkeep)
- ❌ `uploads/` contents (except .gitkeep)
- ❌ Test/debug scripts (`test_*.py`, `debug_*.py`)

**These files SHOULD be listed:**
- ✅ `config.env.example` (template without sensitive data)
- ✅ `.gitignore`
- ✅ `README.md`
- ✅ `requirements.txt`
- ✅ `app.py`
- ✅ All files in `core/`, `templates/`, `static/`
- ✅ Test data files in `Test_Data/`

### After Pushing - Verify on GitHub

1. Go to your repository on GitHub: `https://github.com/YOUR_USERNAME/Python-API-Testing-Framework`
2. Check that:
   - ✅ README.md is displayed on the main page
   - ✅ All necessary files are present
   - ❌ `config.env` is NOT visible (very important!)
   - ✅ `config.env.example` IS visible

---

## Common Issues and Solutions

### Issue 1: "config.env" appears in git status

**Solution:**
```powershell
# Remove config.env from git tracking (if accidentally added)
git rm --cached config.env

# Verify .gitignore includes config.env
# Then commit the change
git commit -m "Remove config.env from tracking"
```

### Issue 2: Authentication Failed

**Solution:**
- Use a Personal Access Token instead of password
- Generate token at: https://github.com/settings/tokens
- Use token as password when prompted

### Issue 3: Remote Already Exists

**Solution:**
```powershell
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/YOUR_USERNAME/HTTPie-Python-Web.git
```

---

## Next Steps After Pushing

1. **Add Repository Description and Topics**
   - Go to repository settings on GitHub
   - Add topics: `flask`, `api-testing`, `python`, `websocket`, `testing-framework`

2. **Enable GitHub Pages (Optional)**
   - If you want to host documentation

3. **Set Up Branch Protection (Optional)**
   - Protect the main branch from force pushes

4. **Add Collaborators (Optional)**
   - Settings → Collaborators → Add people

---

## Useful Git Commands for Future Updates

```powershell
# Check status
git status

# Add specific files
git add filename.py

# Add all changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

## Security Checklist

Before pushing to GitHub, verify:

- [ ] `config.env` is in `.gitignore`
- [ ] `config.env` is NOT in git status
- [ ] `config.env.example` exists with placeholder values
- [ ] No API keys or passwords in any committed files
- [ ] README.md has clear setup instructions
- [ ] Test data files don't contain sensitive information

---

**Need Help?**
- GitHub Docs: https://docs.github.com
- Git Documentation: https://git-scm.com/doc

