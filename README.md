# TOS Tool

**TOS** (The One System) is a personal Swiss knife command-line utility for digital standardization on your working PC. It helps you manage templates, environment shortcuts, and configuration in a centralized way.

## Features

- **Template Management**: Initialize projects with predefined templates
- **Environment Shortcuts**: Quick navigation to frequently used directories
- **Configuration Management**: Centralized TOML config file and CSV-based environment variables
- **Command History**: SQLite-based logging of all TOS command executions
- **Cross-Platform**: Works on Windows, macOS, and Linux with TOS_HOME support

## Installation

### From PyPI (Recommended)

Once published, install from PyPI:

```bash
# Using pip
pip install tos-tool

# Using pipx (isolated installation)
pipx install tos-tool

# Using uv (fastest)
uv tool install tos-tool


uv tool install .  --reinstall      
```

### From GitHub

Install directly from GitHub repository:

```bash
# Using uv
uv tool install git+https://github.com/arunkumaranand/tos_tool.git

# Using pip
pip install git+https://github.com/arunkumaranand/tos_tool.git
```

### From Local Source (Development)

For local development:

```bash
cd tos_tool

# Using uv (editable install)
uv pip install -e .

# Using pip (editable install)
pip install -e .
```

## Configuration

On first run, TOS creates a configuration directory at:
- **Windows**: `%LOCALAPPDATA%\tos` (e.g., `C:\Users\YourName\AppData\Local\tos`)
- **Linux/Mac**: `~/.tos`

You can override the default location by setting the `TOS_HOME` environment variable:
```bash
# Windows
setx TOS_HOME "C:\your\custom\path"

# Linux/Mac
export TOS_HOME="/your/custom/path"
```

The config directory contains:
- `tos_env.csv` - Environment variables (key, value, updated_on, comment)
- `tos_config.toml` - Configuration settings (history_limit, etc.)
- `tos_history.db` - SQLite database with command execution history
- `kb.xlsx` - Knowledge base Excel file (optional)
- `templates/` - Directory for project templates

## Commands

### `tos info`

Display TOS configuration information including paths and file status.

```bash
tos info
```

**Output:**
```
TOS Configuration Information
========================================
Config Directory: C:\Users\YourName\AppData\Roaming\tos
Config File: C:\Users\YourName\AppData\Roaming\tos\tos_config.yml
Templates Directory: C:\Users\YourName\AppData\Roaming\tos\templates
KB File: C:\Users\YourName\AppData\Roaming\tos\kb.xlsx

Files Status:
  tos_config.yml: ✓ exists
  kb.xlsx: ✗ missing
  templates/: ✓ exists
```

### `tos init -t <template_name>`

Initialize the current directory with a template. Copies all files from the template and creates a `.tos` folder with the copied files.

```bash
# Navigate to your project directory
cd d:\myproject

# Initialize with the 'budget' template
tos init -t budget
```

**What it does:**
1. Copies all files from `%APPDATA%\tos\templates\budget\` to current directory
2. Creates `.tos` folder in current directory
3. Stores a copy of template files in `.tos` folder

**Example template structure:**
```
%APPDATA%\tos\templates\budget\
├── budget_template.xlsx
├── README.md
└── config\
    └── settings.json
```

### `tos env`

List all configured environment variables from `tos_config.yml`.

```bash
tos env
```

**Output:**
```
Environment Variables
========================================
tools        = c:\aka\tools
proj_a_code  = d:\aka\projects\project_a\code
downloads    = c:\Users\YourName\Downloads
docs         = c:\Users\YourName\Documents
```

### `tos cd <env_name>`

Generate a command to change directory to a configured environment path.

```bash
tos cd tools
```

**Output:**
```
cd /d c:\aka\tools

# To change directory, run: tos cd tools | cmd
```

**Note:** Due to Windows shell limitations, you need to pipe the output to cmd:

```bash
tos cd tools | cmd
```

Or create an alias/batch file for convenience:

**Create `toscd.bat` in a directory on your PATH:**
```batch
@echo off
for /f "delims=" %%i in ('tos cd %1') do set TOS_CD_CMD=%%i
%TOS_CD_CMD%
```

Then use: `toscd tools`

### `tos history`

Display command execution history from the SQLite database. All TOS commands are automatically logged with timestamp, command name, arguments, working directory, and status.

```bash
# Show recent command history (default: 100 entries)
tos history

# Show limited number of entries
tos history --limit 10

# Filter by specific command
tos history --command env

# Combine filters
tos history --command init --limit 5
```

**Output:**
```
Timestamp            Command         Arguments                      Status     Directory
========================================================================
2025-10-24 11:59:48  history                                        ✓          C:\AKA\Code\_me\tos_tool
2025-10-24 11:59:38  template        list                           ✓          C:\AKA\Code\_me\tos_tool
2025-10-24 11:59:30  env             list                           ✓          C:\AKA\Code\_me\tos_tool
2025-10-24 11:59:19  info                                           ✓          C:\AKA\Code\_me\tos_tool
========================================================================
Showing 4 most recent entries (limit: 100)
```

**Configuration:**
The history limit can be configured in `tos_config.toml`:
```toml
[settings]
history_limit = 100
```

### `tos template list`

List all available templates in the templates directory.

```bash
tos template list
```

### `tos template add <name>`

Save the current directory as a template.

```bash
cd c:\myproject
tos template add myproject

# Force overwrite existing template (creates backup)
tos template add myproject --force
```

### `tos env list`

List all configured environment variables from `tos_env.csv`.

```bash
tos env list
```

### `tos env add <key> <value>`

Add a new environment variable to `tos_env.csv`.

```bash
tos env add tools c:\aka\tools

# Add with a comment
tos env add docs "c:\Users\Me\Documents" --comment "Personal documents"

# Force overwrite existing variable (creates backup)
tos env add tools c:\new\path --force
```

## Creating Templates

1. Navigate to your templates directory:
   ```bash
   cd %APPDATA%\tos\templates
   ```

2. Create a new template directory:
   ```bash
   mkdir mytemplate
   cd mytemplate
   ```

3. Add your template files:
   ```
   mytemplate\
   ├── README.md
   ├── .gitignore
   ├── src\
   │   └── main.py
   └── docs\
       └── guide.md
   ```

4. Use the template:
   ```bash
   cd d:\mynewproject
   tos init -t mytemplate
   ```

## Common Workflows

### Setting Up a New Budget Project

```bash
# Create project directory
mkdir d:\projects\q4_budget
cd d:\projects\q4_budget

# Initialize with budget template
tos init -t budget

# Files are now copied and ready to use
```

### Quick Navigation

```bash
# View available shortcuts
tos env

# Jump to tools directory
tos cd tools | cmd

# Jump to project code
tos cd proj_a_code | cmd
```

### Check Configuration

```bash
# View config info
tos info

# Edit config file
notepad %APPDATA%\tos\tos_config.yml
```

## Development

### Project Structure

```
tos_tool/
├── main.py              # Main CLI application
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

### Requirements

- Python >= 3.8
- click >= 8.1.7
- openpyxl >= 3.1.2

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
