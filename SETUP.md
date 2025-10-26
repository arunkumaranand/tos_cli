# TOS Setup Guide

## Quick Start

### 1. Install TOS

```bash
# From GitHub
uv tool install git+https://github.com/yourusername/tos_tool.git

# Or locally for development
cd c:\AKA\Code\_me\tos_tool
uv pip install -e .
```

### 2. Verify Installation

```bash
tos info
```

This will create the default config directory at `%APPDATA%\tos` and generate a default `tos_config.yml`.

### 3. Set Up Templates

Copy the example budget template to your config directory:

```bash
# Navigate to TOS config directory
cd %APPDATA%\tos\templates

# Create budget template
mkdir budget
cd budget

# Add your template files here
# For example, copy from this project:
xcopy /E /I c:\AKA\Code\_me\tos_tool\example_template\budget\* .
```

### 4. Customize Environment Variables

Edit your config file:

```bash
notepad %APPDATA%\tos\tos_config.yml
```

Add your commonly used directories:

```yaml
environment_variables:
  tools: c:\aka\tools
  proj_a_code: d:\aka\projects\project_a\code
  downloads: c:\Users\YourName\Downloads
  docs: c:\Users\YourName\Documents
  desktop: c:\Users\YourName\Desktop
```

### 5. Test Commands

```bash
# List environment variables
tos env

# View configuration
tos info

# Test template initialization
cd d:\test_project
tos init -t budget

# Test directory navigation
tos cd tools
```

## Creating a Directory Navigation Helper (Optional)

Since `tos cd` can't directly change your shell's directory, create a batch helper:

**Create `toscd.bat` in `C:\Windows\System32` or any directory in your PATH:**

```batch
@echo off
for /f "delims=" %%i in ('tos cd %1') do set TOS_CD_CMD=%%i
%TOS_CD_CMD%
```

Now you can use:

```bash
toscd tools
toscd proj_a_code
```

## Creating More Templates

1. Go to templates directory:
   ```bash
   cd %APPDATA%\tos\templates
   ```

2. Create a new template directory:
   ```bash
   mkdir python_project
   cd python_project
   ```

3. Add template files:
   ```
   python_project/
   ├── README.md
   ├── requirements.txt
   ├── .gitignore
   ├── main.py
   └── tests/
       └── test_main.py
   ```

4. Use it:
   ```bash
   cd d:\mynewproject
   tos init -t python_project
   ```

## Troubleshooting

### Command not found
- Make sure TOS is installed: `uv tool list`
- Try reinstalling: `uv tool uninstall tos-tool && uv tool install git+https://github.com/yourusername/tos_tool.git`

### Template not found
- Check templates directory: `dir %APPDATA%\tos\templates`
- Verify template name matches directory name exactly

### Config file issues
- Check file location: `tos info`
- Edit manually: `notepad %APPDATA%\tos\tos_config.yml`
- Ensure YAML syntax is correct (proper indentation)

## Tips

1. **Backup your config**: Regularly backup `%APPDATA%\tos\` directory
2. **Version control templates**: Keep templates in a git repository
3. **Share templates**: Export template directories to share with team
4. **Environment variables**: Add all frequently accessed directories
5. **Naming conventions**: Use short, memorable names for environment variables

## Advanced Usage

### Syncing Config Across Machines

You can keep your TOS config in a Git repository:

```bash
cd %APPDATA%\tos
git init
git add .
git commit -m "Initial TOS config"
git remote add origin https://github.com/yourusername/tos-config.git
git push -u origin main
```

On another machine:

```bash
# Install TOS
uv tool install git+https://github.com/yourusername/tos_tool.git

# Clone your config
cd %APPDATA%
rmdir /s /q tos
git clone https://github.com/yourusername/tos-config.git tos
```

### Using with PowerShell

Create a PowerShell function in your profile:

```powershell
function toscd($env_name) {
    $path = (tos cd $env_name | Select-Object -First 1).Replace('cd /d ', '')
    Set-Location $path
}
```

Add to your PowerShell profile:

```powershell
notepad $PROFILE
```

Then use:

```powershell
toscd tools
toscd proj_a_code
```
