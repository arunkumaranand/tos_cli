# Setting Up GitHub for TOS Tool

This guide shows how to set up a GitHub repository for your TOS tool so users can install directly from GitHub.

## Why GitHub Installation?

Users can install from GitHub using:
```bash
uv tool install git+https://github.com/yourusername/tos_tool.git
pip install git+https://github.com/yourusername/tos_tool.git
```

This is useful:
- **Before PyPI publishing** - Share your tool while preparing for PyPI
- **Development versions** - Users can install the latest from `main` branch
- **Private tools** - Keep your tool private (only accessible to authorized users)
- **Quick testing** - Let others test without publishing to PyPI

## Step 1: Create GitHub Repository

### Option A: Using GitHub Website

1. Go to [GitHub](https://github.com) and sign in
2. Click the **+** icon in the top right
3. Select **New repository**
4. Configure repository:
   - **Repository name**: `tos_tool`
   - **Description**: "Personal Swiss knife CLI tool for digital standardization"
   - **Visibility**: 
     - `Public` - Anyone can install
     - `Private` - Only you (or collaborators) can install
   - **Initialize**: Don't add README, .gitignore, or license (we already have them)
5. Click **Create repository**

### Option B: Using GitHub CLI

```bash
# Install GitHub CLI first (if not installed)
# Windows: winget install GitHub.cli
# Mac: brew install gh

# Login to GitHub
gh auth login

# Create repository
gh repo create tos_tool --public --description "Personal Swiss knife CLI tool for digital standardization"
```

## Step 2: Initialize Git Locally

Open PowerShell in your project directory:

```powershell
cd c:\AKA\Code\_me\tos_tool

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: TOS CLI tool with environment management, templates, and command history"
```

## Step 3: Connect to GitHub and Push

Replace `yourusername` with your actual GitHub username:

```powershell
# Add remote repository
git remote add origin https://github.com/yourusername/tos_tool.git

# Set default branch name to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### If You're Using SSH

```powershell
# Add remote with SSH
git remote add origin git@github.com:yourusername/tos_tool.git

# Push to GitHub
git push -u origin main
```

## Step 4: Verify on GitHub

1. Go to `https://github.com/yourusername/tos_tool`
2. You should see all your files:
   - `main.py`
   - `pyproject.toml`
   - `README.md`
   - `LICENSE`
   - `PUBLISH.md`
   - etc.

## Step 5: Test Installation from GitHub

Now anyone can install your tool directly from GitHub:

```bash
# Using uv
uv tool install git+https://github.com/yourusername/tos_tool.git

# Using pip
pip install git+https://github.com/yourusername/tos_tool.git

# Using pipx
pipx install git+https://github.com/yourusername/tos_tool.git
```

### Installing Specific Branch or Commit

```bash
# Install from specific branch
uv tool install git+https://github.com/yourusername/tos_tool.git@develop

# Install from specific tag/version
uv tool install git+https://github.com/yourusername/tos_tool.git@v0.1.0

# Install from specific commit
uv tool install git+https://github.com/yourusername/tos_tool.git@abc123
```

## Updating Your Repository

After making changes to your code:

```powershell
# Check what changed
git status

# Add changed files
git add .

# Or add specific files
git add main.py README.md

# Commit changes
git commit -m "Add new feature: XYZ"

# Push to GitHub
git push
```

## Creating Releases/Tags

Tags are useful for marking specific versions:

```powershell
# Create a tag for version 0.1.0
git tag v0.1.0

# Push tag to GitHub
git push origin v0.1.0

# Or push all tags
git push --tags
```

Then users can install specific versions:
```bash
uv tool install git+https://github.com/yourusername/tos_tool.git@v0.1.0
```

## Private Repository Access

If your repository is private, users need authentication:

### Using SSH (Recommended for private repos)

```bash
# Setup SSH key with GitHub first
# Then install using SSH URL
uv tool install git+ssh://git@github.com/yourusername/tos_tool.git
```

### Using Personal Access Token

```bash
# Install with token
uv tool install git+https://username:TOKEN@github.com/yourusername/tos_tool.git
```

## Best Practices

### 1. Update README URLs

After creating the GitHub repo, update these in `pyproject.toml`:

```toml
[project.urls]
Homepage = "https://github.com/yourusername/tos_tool"
Repository = "https://github.com/yourusername/tos_tool"
Issues = "https://github.com/yourusername/tos_tool/issues"
Documentation = "https://github.com/yourusername/tos_tool/blob/main/README.md"
```

And in `README.md`, update the installation command.

### 2. Add GitHub Topics

Add topics to your GitHub repository for discoverability:
- `cli`
- `productivity`
- `python`
- `tool`
- `environment-management`
- `templates`

Go to your repo → About section (gear icon) → Add topics

### 3. Create a Good README

Your README should include (already done! ✓):
- Clear description
- Installation instructions
- Usage examples
- Features list

### 4. Add Branch Protection (Optional)

For main branch:
1. Go to Settings → Branches
2. Add branch protection rule for `main`
3. Require pull requests before merging
4. Require status checks to pass

## Comparison: GitHub vs PyPI Installation

| Aspect | GitHub Installation | PyPI Installation |
|--------|-------------------|-------------------|
| **Before publishing** | ✅ Available immediately | ❌ Must publish first |
| **Development versions** | ✅ Always latest code | ❌ Only released versions |
| **Easy updates** | `git push` | Rebuild + upload to PyPI |
| **Discoverability** | ❌ Users need the URL | ✅ Searchable on PyPI |
| **Version management** | Manual (tags/branches) | ✅ Automatic versioning |
| **Installation speed** | Slower (clones repo) | ✅ Faster (pre-built wheel) |
| **Best for** | Development, private tools | ✅ Public release, stable versions |

## Recommended Workflow

1. **Development**: Work locally, commit to GitHub frequently
2. **Testing**: Share GitHub link with testers
   ```bash
   uv tool install git+https://github.com/yourusername/tos_tool.git
   ```
3. **Release**: When stable, publish to PyPI
   ```bash
   python -m build
   python -m twine upload dist/*
   ```
4. **Users**: Install from PyPI for stable releases
   ```bash
   uv tool install tos-tool
   ```
5. **Power users**: Can still use GitHub for latest features
   ```bash
   uv tool install git+https://github.com/yourusername/tos_tool.git
   ```

## Quick Reference Commands

```powershell
# Initial setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/tos_tool.git
git push -u origin main

# Regular updates
git add .
git commit -m "Your commit message"
git push

# Create release tag
git tag v0.1.0
git push origin v0.1.0

# Installation commands users can use
# From GitHub:
uv tool install git+https://github.com/yourusername/tos_tool.git

# From PyPI (after publishing):
uv tool install tos-tool
```

## Troubleshooting

### "Permission denied" when pushing

- Make sure you're authenticated with GitHub
- Use `gh auth login` or set up SSH keys
- Or use Personal Access Token

### "Repository not found"

- Check the URL is correct
- Ensure repository is public or you have access
- Try refreshing credentials: `gh auth refresh`

### "fatal: not a git repository"

- Run `git init` first in your project directory

### Installation fails from GitHub

- Check `pyproject.toml` is properly configured
- Ensure all dependencies are listed
- Try installing dependencies manually first

---

Now your tool can be installed from GitHub! 🚀
