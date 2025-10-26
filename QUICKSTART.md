# TOS Quick Start Guide

## Installation

```bash
# Install with uv from GitHub (once published)
uv tool install git+https://github.com/yourusername/tos_tool.git

# Or install locally for testing
cd c:\AKA\Code\_me\tos_tool
uv pip install -e .
```

## First Time Setup

1. **Initialize TOS**
   ```bash
   python main.py info
   ```
   This creates `%APPDATA%\tos` with default config.

2. **Copy Example Template**
   ```powershell
   Copy-Item -Path "c:\AKA\Code\_me\tos_tool\example_template\budget" -Destination "$env:APPDATA\tos\templates\budget" -Recurse
   ```

3. **Edit Configuration**
   ```bash
   notepad %APPDATA%\tos\tos_config.yml
   ```
   
   Add your directories:
   ```yaml
   environment_variables:
     tools: c:\aka\tools
     code: d:\projects\code
     docs: c:\Users\YourName\Documents
   ```

## Basic Usage

### View Info
```bash
python main.py info
```

### List Environment Variables
```bash
python main.py env
```

### Navigate to Directory
```bash
python main.py cd tools
# Copy the output and paste it, or use: python main.py cd tools | cmd
```

### Initialize Project with Template
```bash
cd d:\myproject
python main.py init -t budget
```

## Create Your Own Template

1. Create template directory:
   ```powershell
   mkdir "$env:APPDATA\tos\templates\mytemplate"
   cd "$env:APPDATA\tos\templates\mytemplate"
   ```

2. Add your files:
   ```
   mytemplate/
   ├── README.md
   ├── config.json
   └── scripts/
       └── setup.ps1
   ```

3. Use it:
   ```bash
   cd d:\newproject
   python main.py init -t mytemplate
   ```

## Tips

**Create a CD Helper (PowerShell)**

Add to your PowerShell profile (`$PROFILE`):
```powershell
function toscd($env_name) {
    $path = (python c:\AKA\Code\_me\tos_tool\main.py cd $env_name | Select-Object -First 1).Replace('cd /d ', '')
    Set-Location $path
}
```

Usage: `toscd tools`

**Create a CD Helper (Batch)**

Create `toscd.bat` in a directory on your PATH:
```batch
@echo off
for /f "delims=" %%i in ('python c:\AKA\Code\_me\tos_tool\main.py cd %1') do set TOS_CD_CMD=%%i
%TOS_CD_CMD%
```

Usage: `toscd tools`

## Configuration File Location

- **Windows**: `%APPDATA%\tos\tos_config.yml`
- **Templates**: `%APPDATA%\tos\templates\`
- **KB File**: `%APPDATA%\tos\kb.xlsx`

## All Commands

| Command | Description |
|---------|-------------|
| `python main.py info` | Show configuration paths and status |
| `python main.py env` | List all environment variables |
| `python main.py cd <name>` | Generate cd command for environment |
| `python main.py init -t <template>` | Initialize current directory with template |
| `python main.py --help` | Show help message |

## Example Workflow

```bash
# 1. Setup TOS
python main.py info

# 2. View shortcuts
python main.py env

# 3. Create new project
mkdir d:\projects\budget_2025
cd d:\projects\budget_2025

# 4. Initialize with template
python main.py init -t budget

# 5. Start working!
dir
# Shows: README.md, notes.txt, .gitignore, .tos/
```
