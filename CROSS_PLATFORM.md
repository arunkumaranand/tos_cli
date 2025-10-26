# TOS Cross-Platform Usage

TOS is designed to work seamlessly across Windows, macOS, and Linux.

## Configuration Location

### Default Locations

TOS automatically uses platform-appropriate default locations:

**Windows:**
- `%LOCALAPPDATA%\tos`
- Example: `C:\Users\YourName\AppData\Local\tos`

**macOS:**
- `~/.tos`
- Example: `/Users/username/.tos`

**Linux:**
- `~/.tos`
- Example: `/home/username/.tos`

### Custom Location (TOS_HOME)

You can override the default location by setting the `TOS_HOME` environment variable:

**Windows (PowerShell):**
```powershell
# Temporary (current session only)
$env:TOS_HOME = "C:\your\custom\path"

# Permanent
setx TOS_HOME "C:\your\custom\path"
```

**Windows (CMD):**
```cmd
rem Permanent
setx TOS_HOME "C:\your\custom\path"
```

**macOS/Linux (Bash):**
```bash
# Temporary (current session only)
export TOS_HOME="/your/custom/path"

# Permanent (add to ~/.bashrc or ~/.bash_profile)
echo 'export TOS_HOME="/your/custom/path"' >> ~/.bashrc
source ~/.bashrc
```

**macOS/Linux (Zsh):**
```zsh
# Permanent (add to ~/.zshrc)
echo 'export TOS_HOME="/your/custom/path"' >> ~/.zshrc
source ~/.zshrc
```

## Configuration Files

Regardless of platform, TOS creates these files in the config directory:

```
<config_dir>/
├── tos_env.csv          # Environment variables
├── kb.xlsx              # Knowledge base (optional)
└── templates/           # Project templates
    ├── budget/
    ├── myproject/
    └── ...
```

## Platform-Specific Considerations

### Path Separators

TOS automatically handles path separators for each platform:
- Windows: `\` or `/` (both work)
- macOS/Linux: `/`

When adding environment variables, use the natural path format for your OS:

```bash
# Windows
tos env add -k projects -v "C:\Users\YourName\Projects"

# macOS/Linux
tos env add -k projects -v "/Users/username/Projects"
```

### Directory Navigation (tos cd)

The `tos cd` command behavior varies by platform and shell:

**Windows (PowerShell):**
```powershell
# Create helper function (add to $PROFILE)
function toscd($name) {
    $path = (.venv\Scripts\tos cd $name | Select-Object -First 1).Replace('cd /d ', '')
    Set-Location $path
}
```

**Windows (CMD):**
```cmd
rem Create toscd.bat
@echo off
for /f "delims=" %%i in ('tos cd %1') do set TOS_CD_CMD=%%i
%TOS_CD_CMD%
```

**macOS/Linux (Bash/Zsh):**
```bash
# Add to ~/.bashrc or ~/.zshrc
toscd() {
    local path=$(tos cd "$1" 2>/dev/null | head -n 1 | sed 's/cd -d //')
    if [ -n "$path" ]; then
        cd "$path"
    fi
}
```

## Syncing Config Across Machines

### Using Git

```bash
# Initialize git in config directory
cd ~/.tos  # or your TOS_HOME
git init
git add tos_env.csv templates/
git commit -m "Initial TOS config"
git remote add origin <your-repo-url>
git push -u origin main
```

### Using Cloud Storage

Set `TOS_HOME` to a cloud-synced directory:

**Dropbox:**
- Windows: `setx TOS_HOME "%USERPROFILE%\Dropbox\tos"`
- macOS/Linux: `export TOS_HOME="$HOME/Dropbox/tos"`

**OneDrive:**
- Windows: `setx TOS_HOME "%OneDrive%\tos"`

**Google Drive:**
- macOS: `export TOS_HOME="$HOME/Google Drive/tos"`
- Linux: `export TOS_HOME="$HOME/GoogleDrive/tos"`

## Checking Configuration

To verify your TOS configuration on any platform:

```bash
tos info
```

This displays:
- Current `TOS_HOME` setting
- Config directory location
- Platform information
- File status
- Instructions for setting `TOS_HOME`

## Example: Multi-Platform Setup

If you work on both Windows and macOS:

1. **Set a cloud-synced TOS_HOME** on both machines
2. **Use relative paths** or environment-specific entries
3. **Create platform-specific templates** when needed

```csv
# tos_env.csv with platform-aware entries
key,value,updated_on,comment
projects_win,C:\Users\John\Projects,2025-10-24 10:00:00,Windows projects
projects_mac,/Users/john/Projects,2025-10-24 10:00:00,macOS projects
shared_docs,~/Documents/Shared,2025-10-24 10:00:00,Works on all platforms
```

## Installation

TOS can be installed the same way on all platforms:

```bash
# Using uv (recommended)
uv tool install git+https://github.com/yourusername/tos_tool.git

# Or locally for development
cd tos_tool
uv pip install -e .
```

## Platform-Tested Features

All TOS features work identically across platforms:

✅ `tos info` - Configuration info
✅ `tos env` - List variables
✅ `tos env add` - Add variables
✅ `tos cd <name>` - Directory navigation (with helper)
✅ `tos template list` - List templates
✅ `tos template add` - Add templates
✅ `tos init -t <name>` - Initialize with template
