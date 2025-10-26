# Publishing TOS to PyPI

This guide walks you through publishing the TOS tool to PyPI (Python Package Index) and installing it as a command-line tool.

## Prerequisites

1. **PyPI Account**: Create accounts at:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing, recommended first)

2. **Install Build Tools**:
   ```bash
   pip install build twine
   ```

3. **API Token**: Generate API tokens for authentication:
   - Go to [PyPI Account Settings](https://pypi.org/manage/account/)
   - Click "Add API token"
   - Set scope to "Entire account" (or specific project later)
   - **Save the token** - you'll only see it once!

## Step 1: Prepare Your Package

### 1.1 Verify `pyproject.toml`

Ensure your `pyproject.toml` is properly configured:

```toml
[project]
name = "tos-tool"  # Must be unique on PyPI
version = "0.1.0"  # Semantic versioning
description = "Personal Swiss knife CLI tool for digital standardization"
readme = "README.md"
requires-python = ">=3.13"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["cli", "productivity", "environment", "templates"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.13",
    "Environment :: Console",
    "Topic :: Utilities",
]

dependencies = [
    "click>=8.1.7",
]

[project.urls]
Homepage = "https://github.com/yourusername/tos_tool"
Repository = "https://github.com/yourusername/tos_tool"
Issues = "https://github.com/yourusername/tos_tool/issues"

[project.scripts]
tos = "tos_tool.main:cli"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["tos_tool"]
```

### 1.2 Reorganize Project Structure

Your package needs to be in a proper Python package structure:

```
tos_tool/                    # Root directory
├── tos_tool/                # Package directory
│   ├── __init__.py          # Makes it a package
│   └── main.py              # Your CLI code
├── pyproject.toml
├── README.md
├── LICENSE                  # Add a license file
└── PUBLISH.md              # This guide
```

**Actions needed:**

1. Create the package directory:
   ```bash
   mkdir tos_tool\tos_tool
   ```

2. Move `main.py` into the package:
   ```bash
   move main.py tos_tool\main.py
   ```

3. Create `tos_tool\__init__.py`:
   ```python
   """TOS - Personal Swiss knife tool for digital standardization."""
   
   __version__ = "0.1.0"
   ```

4. Create `LICENSE` file (example MIT License):
   ```text
   MIT License

   Copyright (c) 2025 Your Name

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
   ```

### 1.3 Create `.pypirc` for Authentication

Create `%USERPROFILE%\.pypirc` (Windows) or `~/.pypirc` (Linux/Mac):

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YourActualAPITokenHere

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YourTestAPITokenHere
```

**Security Note**: Keep this file private! Add to `.gitignore`.

## Step 2: Build the Package

### 2.1 Clean Previous Builds

```bash
# Remove old build artifacts
rmdir /s /q dist
rmdir /s /q build
rmdir /s /q tos_tool.egg-info
```

### 2.2 Build Distribution Files

```bash
# Navigate to project root
cd c:\AKA\Code\_me\tos_tool

# Build the package
python -m build
```

This creates two files in `dist/`:
- `tos_tool-0.1.0.tar.gz` (source distribution)
- `tos_tool-0.1.0-py3-none-any.whl` (wheel distribution)

### 2.3 Verify the Build

```bash
# Check package contents
tar -tzf dist\tos_tool-0.1.0.tar.gz

# Verify wheel
pip install check-wheel-contents
check-wheel-contents dist\tos_tool-0.1.0-py3-none-any.whl
```

## Step 3: Test on TestPyPI (Recommended)

### 3.1 Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

### 3.2 Test Installation from TestPyPI

```bash
# Create a test virtual environment
python -m venv test_env
test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps tos-tool

# Test the command
tos --help
tos info

# Deactivate and remove test environment
deactivate
rmdir /s /q test_env
```

## Step 4: Publish to PyPI (Production)

### 4.1 Upload to PyPI

```bash
python -m twine upload dist/*
```

You'll see output like:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading tos_tool-0.1.0-py3-none-any.whl
Uploading tos_tool-0.1.0.tar.gz
```

### 4.2 Verify on PyPI

Visit: https://pypi.org/project/tos-tool/

## Step 5: Installation Methods

### Method 1: Install with pip (Recommended)

```bash
pip install tos-tool
```

### Method 2: Install with pipx (Isolated)

```bash
# Install pipx if not already installed
pip install pipx
pipx ensurepath

# Install TOS
pipx install tos-tool

# Upgrade later
pipx upgrade tos-tool

# Uninstall
pipx uninstall tos-tool
```

### Method 3: Install with uv (Fast)

```bash
# Install uv if not already installed
pip install uv

# Install TOS
uv tool install tos-tool

# Upgrade later
uv tool upgrade tos-tool

# Uninstall
uv tool uninstall tos-tool
```

### Method 4: Development Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/tos_tool.git
cd tos_tool

# Install in editable mode
pip install -e .

# Or with uv
uv pip install -e .
```

## Step 6: Verify Installation

After installation with any method:

```bash
# Check if command is available
tos --help

# Verify version
tos info

# Test functionality
tos env list
tos history
```

## Updating Your Package

### 6.1 Update Version Number

Edit `pyproject.toml` and `tos_tool/__init__.py`:

```toml
version = "0.1.1"  # Increment version
```

```python
__version__ = "0.1.1"
```

### 6.2 Rebuild and Upload

```bash
# Clean old builds
rmdir /s /q dist

# Build new version
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

### 6.3 Version Numbering Guide

Follow [Semantic Versioning](https://semver.org/):

- `0.1.0` → `0.1.1` - Bug fixes (PATCH)
- `0.1.0` → `0.2.0` - New features, backward compatible (MINOR)
- `0.1.0` → `1.0.0` - Breaking changes (MAJOR)

## Troubleshooting

### Package Name Already Exists

If `tos-tool` is taken, choose another name:
- `tos-cli`
- `tos-personal`
- `yourname-tos`

Update in `pyproject.toml`:
```toml
name = "tos-cli"  # New name
```

### Command Not Found After Installation

```bash
# Verify installation
pip show tos-tool

# Check if Scripts directory is in PATH
# Windows: Add %APPDATA%\Python\Python313\Scripts to PATH
# Linux/Mac: Ensure ~/.local/bin is in PATH
```

### Upload Fails with Authentication Error

```bash
# Use token directly
python -m twine upload dist/* --username __token__ --password pypi-YourTokenHere
```

### Import Errors After Installation

Ensure package structure is correct:
```
tos_tool/
├── tos_tool/           # Package folder (must match name in pyproject.toml)
│   ├── __init__.py
│   └── main.py
└── pyproject.toml
```

## Best Practices

1. **Always test on TestPyPI first** before publishing to production PyPI
2. **Use API tokens** instead of passwords for authentication
3. **Version your releases** - you cannot re-upload the same version number
4. **Write good README.md** - it's displayed on your PyPI page
5. **Add classifiers** - helps users find your package
6. **Include LICENSE** - makes it clear how others can use your code
7. **Tag releases in Git**:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

## Quick Reference Commands

```bash
# Full publish workflow
rmdir /s /q dist
python -m build
python -m twine upload --repository testpypi dist/*  # Test first
python -m twine upload dist/*                         # Production

# Install
pip install tos-tool
pipx install tos-tool
uv tool install tos-tool

# Upgrade
pip install --upgrade tos-tool
pipx upgrade tos-tool
uv tool upgrade tos-tool

# Uninstall
pip uninstall tos-tool
pipx uninstall tos-tool
uv tool uninstall tos-tool
```

## Additional Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Semantic Versioning](https://semver.org/)
- [Choose a License](https://choosealicense.com/)
