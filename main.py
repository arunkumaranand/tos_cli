import os
import shutil
import csv
import platform
import sqlite3
import sys
from pathlib import Path
from datetime import datetime
import click
import fnmatch


def get_config_dir():
    """Get the TOS configuration directory path.
    
    Priority:
    1. TOS_HOME environment variable (if set)
    2. Platform-specific default location:
       - Windows: %LOCALAPPDATA%/tos or %USERPROFILE%/.tos
       - macOS: ~/.tos
       - Linux: ~/.tos
    """
    # Check if TOS_HOME is set
    tos_home = os.getenv('TOS_HOME')
    if tos_home:
        return Path(tos_home)
    
    # Platform-specific defaults
    system = platform.system()
    home = Path.home()
    
    if system == 'Windows':
        # Use LOCALAPPDATA on Windows (better for portable data)
        local_appdata = os.getenv('LOCALAPPDATA')
        if local_appdata:
            return Path(local_appdata) / 'tos'
        # Fallback to home directory
        return home / '.tos'
    else:
        # macOS and Linux use ~/.tos
        return home / '.tos'


def get_env_file():
    """Get the TOS environment variables file path."""
    return get_config_dir() / 'tos_env.csv'


def get_config_toml_file():
    """Get the TOS configuration TOML file path."""
    return get_config_dir() / 'tos_config.toml'


def get_db_file():
    """Get the TOS SQLite database file path."""
    return get_config_dir() / 'tos_history.db'


def init_db():
    """Initialize the SQLite database for command history."""
    db_file = get_db_file()
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create command_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS command_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            command TEXT NOT NULL,
            arguments TEXT,
            working_directory TEXT,
            status TEXT DEFAULT 'success'
        )
    ''')
    
    # Create indexes for better query performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_timestamp 
        ON command_history(timestamp DESC)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_command 
        ON command_history(command)
    ''')
    
    conn.commit()
    conn.close()


def log_command(command, arguments=None, status='success'):
    """Log a command execution to the database."""
    try:
        init_db()  # Ensure DB exists
        db_file = get_db_file()
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO command_history (timestamp, command, arguments, working_directory, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            command,
            arguments or '',
            str(Path.cwd()),
            status
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        # Don't fail if logging fails
        pass


def load_config_toml():
    """Load the TOS configuration from TOML file."""
    config_file = get_config_toml_file()
    
    # Default configuration
    default_config = {
        'history_limit': 100
    }
    
    if not config_file.exists():
        return default_config
    
    try:
        import tomllib
        with open(config_file, 'rb') as f:
            config = tomllib.load(f)
            return {**default_config, **config}
    except Exception:
        return default_config


def ensure_config_exists():
    """Ensure config directory and default configuration files exist."""
    config_dir = get_config_dir()
    env_file = get_env_file()
    config_toml = get_config_toml_file()
    
    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Create templates directory
    templates_dir = config_dir / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # Create default config TOML if it doesn't exist
    if not config_toml.exists():
        default_toml = '''# TOS Configuration File

[settings]
# Maximum number of history entries to display per page
history_limit = 100
'''
        with open(config_toml, 'w', encoding='utf-8') as f:
            f.write(default_toml)
    
    # Create default environment CSV file if it doesn't exist
    if not env_file.exists():
        with open(env_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['key', 'value', 'updated_on', 'comment'])
            writer.writeheader()
            # Add default entries
            writer.writerow({
                'key': 'tools',
                'value': 'c:\\aka\\tools',
                'updated_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'comment': 'Development tools'
            })
            writer.writerow({
                'key': 'proj_a_code',
                'value': 'd:\\aka\\projects\\project_a\\code',
                'updated_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'comment': 'Project A code directory'
            })
    
    return config_dir, env_file


def load_env_config():
    """Load the TOS environment configuration from CSV file."""
    ensure_config_exists()
    env_file = get_env_file()
    
    env_vars = {}
    with open(env_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            env_vars[row['key']] = row['value']
    
    return env_vars


def _resolve_env_key_case_insensitive(env_vars, name):
    """Return the actual key in env_vars matching name, case-insensitive.

    If no match, returns None.
    """
    lname = name.lower()
    for k in env_vars.keys():
        if k.lower() == lname:
            return k
    return None


def add_env_variable(key, value, comment=None, force=False):
    """Add an environment variable to the CSV file."""
    ensure_config_exists()
    env_file = get_env_file()
    
    # Read existing entries
    rows = []
    key_exists = False
    
    with open(env_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['key'] == key:
                key_exists = True
                if not force:
                    return False, f"Environment variable '{key}' already exists with value: {row['value']}"
                # Skip this row if force=True (will be replaced)
            else:
                rows.append(row)
    
    # Add the new/updated entry
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rows.append({
        'key': key,
        'value': value,
        'updated_on': timestamp,
        'comment': comment or ''
    })
    
    # Write all entries back
    with open(env_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['key', 'value', 'updated_on', 'comment'])
        writer.writeheader()
        writer.writerows(rows)
    
    action = "Updated" if key_exists else "Added"
    return True, f"{action} environment variable '{key}' = '{value}'"


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """TOS - Personal Swiss knife tool for digital standardization."""
    # Initialize database on first run
    init_db()
    
    # Log the command execution (but not for --help)
    if ctx.invoked_subcommand and '--help' not in sys.argv:
        command = ctx.invoked_subcommand
        # Get arguments (everything after the command)
        args = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ''
        log_command(command, args)


@cli.command()
def info():
    """Display TOS configuration information."""
    config_dir, env_file = ensure_config_exists()
    
    click.echo("TOS Configuration Information")
    click.echo("=" * 40)
    
    # Show TOS_HOME status
    tos_home = os.getenv('TOS_HOME')
    if tos_home:
        click.echo(f"TOS_HOME: {tos_home} (set)")
    else:
        click.echo(f"TOS_HOME: (not set, using default)")
    
    click.echo(f"Config Directory: {config_dir}")
    click.echo(f"Platform: {platform.system()}")
    click.echo(f"\nEnvironment File: {env_file}")
    click.echo(f"Config File: {get_config_toml_file()}")
    click.echo(f"History Database: {get_db_file()}")
    click.echo(f"Templates Directory: {config_dir / 'templates'}")
    click.echo(f"KB File: {config_dir / 'kb.xlsx'}")
    
    # Check if files exist
    click.echo("\nFiles Status:")
    click.echo(f"  tos_env.csv: {'✓ exists' if env_file.exists() else '✗ missing'}")
    click.echo(f"  tos_config.toml: {'✓ exists' if get_config_toml_file().exists() else '✗ missing'}")
    click.echo(f"  tos_history.db: {'✓ exists' if get_db_file().exists() else '✗ missing'}")
    click.echo(f"  kb.xlsx: {'✓ exists' if (config_dir / 'kb.xlsx').exists() else '✗ missing'}")
    click.echo(f"  templates/: {'✓ exists' if (config_dir / 'templates').exists() else '✗ missing'}")
    
    # Show how to set TOS_HOME
    if not tos_home:
        click.echo(f"\nTo set custom location, use:")
        if platform.system() == 'Windows':
            click.echo(f"  setx TOS_HOME \"C:\\your\\custom\\path\"")
        else:
            click.echo(f"  export TOS_HOME=\"/your/custom/path\"")
            click.echo(f"  # Add to ~/.bashrc or ~/.zshrc to persist")


@cli.command()
@click.option('-t', '--template', required=True, help='Template name to initialize')
@click.option('--force', is_flag=True, help='Force initialization even if directory is not empty')
def init(template, force):
    """Initialize current directory with a template."""
    config_dir = get_config_dir()
    template_dir = config_dir / 'templates' / template
    
    if not template_dir.exists():
        click.echo(f"Error: Template '{template}' not found in {config_dir / 'templates'}", err=True)
        click.echo(f"Available templates: {', '.join([d.name for d in (config_dir / 'templates').iterdir() if d.is_dir()])}")
        return
    
    current_dir = Path.cwd()
    
    # Check if directory is empty (excluding .tos directory)
    existing_items = [item for item in current_dir.iterdir() if item.name != '.tos']
    
    if existing_items and not force:
        click.echo(f"Error: Directory is not empty ({len(existing_items)} item(s) found)", err=True)
        click.echo("Use --force to initialize anyway (will overwrite conflicting files)")
        click.echo("\nExisting items:")
        for item in existing_items[:5]:  # Show first 5 items
            click.echo(f"  - {item.name}")
        if len(existing_items) > 5:
            click.echo(f"  ... and {len(existing_items) - 5} more")
        return
    
    tos_dir = current_dir / '.tos'
    
    # Create .tos directory
    tos_dir.mkdir(exist_ok=True)
    
    # Copy template contents to current directory
    copied_files = []
    overwritten_files = []
    copied_dirs_count = 0
    
    # Ensure all directories and files (including hidden) are copied
    for root, dirs, files in os.walk(template_dir):
        root_path = Path(root)
        rel_root = root_path.relative_to(template_dir)

        # Create corresponding directories in both destinations
        for d in dirs:
            (current_dir / rel_root / d).mkdir(parents=True, exist_ok=True)
            (tos_dir / rel_root / d).mkdir(parents=True, exist_ok=True)
            copied_dirs_count += 1

        # Copy files and track overwrite/new
        for f in files:
            src_file = root_path / f
            relative_path = src_file.relative_to(template_dir)
            dest_file = current_dir / relative_path

            file_exists = dest_file.exists()

            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dest_file)

            if file_exists:
                overwritten_files.append(relative_path)
            else:
                copied_files.append(relative_path)

            tos_dest = tos_dir / relative_path
            tos_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, tos_dest)
    
    click.echo(f"✓ Initialized '{template}' template in {current_dir}")
    click.echo(f"✓ Created .tos directory")
    click.echo(f"✓ Copied {len(copied_files)} file(s)")
    
    click.echo(f"  Directories: {copied_dirs_count}")
    if overwritten_files:
        click.echo(f"✓ Overwritten {len(overwritten_files)} file(s)")
    
    if copied_files:
        click.echo("\nNew files:")
        for file in copied_files:
            click.echo(f"  - {file}")
    
    if overwritten_files:
        click.echo("\nOverwritten files:")
        for file in overwritten_files:
            click.echo(f"  - {file}")


@cli.group()
def template():
    """Manage templates."""
    pass


@template.command('list')
def template_list():
    """List all available templates."""
    config_dir = get_config_dir()
    templates_dir = config_dir / 'templates'
    
    if not templates_dir.exists():
        click.echo(f"Templates directory not found: {templates_dir}")
        return
    
    # Get all subdirectories in templates folder
    template_list = [d.name for d in templates_dir.iterdir() if d.is_dir()]
    
    if not template_list:
        click.echo("No templates available")
        click.echo(f"\nCreate templates in: {templates_dir}")
        return
    
    click.echo("Available Templates")
    click.echo("=" * 40)
    
    for template_name in sorted(template_list):
        template_path = templates_dir / template_name
        # Count files in template
        file_count = sum(1 for _ in template_path.rglob('*') if _.is_file())
        click.echo(f"  {template_name} ({file_count} file(s))")
    
    click.echo(f"\nTemplates location: {templates_dir}")
    click.echo(f"Usage: tos init -t <template_name>")


@template.command('add')
@click.option('-n', '--name', required=True, help='Template name')
@click.option('--force', is_flag=True, help='Overwrite existing template (backs up old version)')
def template_add(name, force):
    """Add current directory as a template."""
    config_dir = get_config_dir()
    templates_dir = config_dir / 'templates'
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    current_dir = Path.cwd()
    template_dest = templates_dir / name
    
    # Check if template already exists
    if template_dest.exists():
        if not force:
            click.echo(f"Error: Template '{name}' already exists", err=True)
            click.echo(f"Use --force to overwrite (will backup existing template)")
            return
        
        # Backup existing template with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{name}_{timestamp}"
        backup_dest = templates_dir / backup_name
        
        click.echo(f"Backing up existing template to: {backup_name}")
        shutil.move(str(template_dest), str(backup_dest))
    
    # Copy current directory to templates
    try:
        # Get list of files to copy (excluding common ignore patterns)
        ignore_patterns = {'.git', '.venv', '__pycache__', '*.pyc', '.tos', 'node_modules'}
        
        def ignore_func(dir, files):
            ignored = []
            for file in files:
                if file in ignore_patterns or any(file.endswith(pattern.replace('*', '')) for pattern in ignore_patterns if '*' in pattern):
                    ignored.append(file)
            return ignored
        
        shutil.copytree(current_dir, template_dest, ignore=ignore_func)
        
        # Count copied files and directories (includes hidden)
        files_count = 0
        dirs_count = 0
        for _, dirs, files in os.walk(template_dest):
            dirs_count += len(dirs)
            files_count += len(files)

        click.echo(f"✓ Template '{name}' created successfully")
        click.echo(f"✓ Copied {files_count} file(s) and {dirs_count} directorie(s) from {current_dir}")
        click.echo(f"✓ Template location: {template_dest}")
        click.echo(f"\nUsage: tos init -t {name}")
        
    except Exception as e:
        click.echo(f"Error creating template: {e}", err=True)
        # Clean up partial copy if it exists
        if template_dest.exists():
            shutil.rmtree(template_dest)


@cli.group(invoke_without_command=True)
@click.pass_context
def env(ctx):
    """Manage environment variables."""
    # If no subcommand is provided, default to list
    if ctx.invoked_subcommand is None:
        ctx.invoke(env_list)


@env.command('list')
def env_list():
    """List all configured environment variables."""
    try:
        env_vars = load_env_config()
        
        if not env_vars:
            click.echo("No environment variables configured in tos_env.csv")
            return
        
        click.echo("Environment Variables")
        click.echo("=" * 40)
        
        # Sort keys case-insensitively for consistent display
        sorted_keys = sorted(env_vars.keys(), key=lambda k: k.lower())
        max_key_len = max(len(key) for key in sorted_keys)
        for key in sorted_keys:
            value = env_vars[key]
            click.echo(f"{key.ljust(max_key_len)} = {value}")
    
    except Exception as e:
        click.echo(f"Error loading environment config: {e}", err=True)


@env.command('add')
@click.option('-k', '--key', required=True, help='Environment variable key/name')
@click.option('-v', '--value', required=True, help='Directory path value')
@click.option('-c', '--comment', help='Optional comment for this variable')
@click.option('--force', is_flag=True, help='Overwrite if key already exists')
def env_add(key, value, comment, force):
    """Add a new environment variable."""
    try:
        success, message = add_env_variable(key, value, comment, force)
        
        if success:
            click.echo(f"✓ {message}")
            click.echo(f"\nUsage: tos cd {key}")
        else:
            click.echo(f"Error: {message}", err=True)
            click.echo("Use --force to overwrite the existing value")
    
    except Exception as e:
        click.echo(f"Error adding environment variable: {e}", err=True)


@env.command('like')
@click.argument('patterns', nargs=-1, required=True)
def env_like(patterns):
    """Search env variable names by wildcard pattern(s) (case-insensitive).

    Examples:
      t env like a*
      t env like *_home
      t env like a* *code*
    """
    try:
        env_vars = load_env_config()
        if not env_vars:
            click.echo("No environment variables configured in tos_env.csv")
            return

        # Normalize patterns list
        if len(patterns) == 1:
            pattern_list = [patterns[0]]
        else:
            pattern_list = list(patterns)

        # Case-insensitive wildcard match on keys for any of the provided patterns
        lowered_keys = {k: k.lower() for k in env_vars.keys()}
        lowered_patterns = [p.lower() for p in pattern_list]
        matched = []
        for k, lk in lowered_keys.items():
            if any(fnmatch.fnmatch(lk, lp) for lp in lowered_patterns):
                matched.append(k)

        if not matched:
            click.echo("No matches.")
            return

        matches = sorted(matched, key=lambda k: k.lower())
        max_key_len = max(len(k) for k in matches)
        if len(pattern_list) == 1:
            click.echo(f"Matches for pattern: {pattern_list[0]}")
        else:
            click.echo(f"Matches for patterns: {' '.join(pattern_list)}")
        click.echo("=" * 40)
        for k in matches:
            click.echo(f"{k.ljust(max_key_len)} = {env_vars[k]}")

    except Exception as e:
        click.echo(f"Error filtering environment variables: {e}", err=True)


@cli.command()
@click.argument('env_name')
def cd(env_name):
    """Change directory to configured environment path.
    
    Note: Due to shell limitations, this command outputs a command that you need to execute.
    Usage: tos cd <env_name> will output the cd command for you to run.
    """
    try:
        env_vars = load_env_config()

        match_key = _resolve_env_key_case_insensitive(env_vars, env_name)
        if not match_key:
            click.echo(f"Error: Environment variable '{env_name}' not found", err=True)
            click.echo(f"Available: {', '.join(env_vars.keys())}")
            return

        path = env_vars[match_key]
        
        # Check if path exists
        if not Path(path).exists():
            click.echo(f"Warning: Path does not exist: {path}", err=True)
        
        # Output shell-specific commands users can evaluate
        shell = os.getenv('PSModulePath')
        if shell:
            click.echo(f"Set-Location -Path \"{path}\"")
            click.echo(f"\n# PowerShell: t cd {env_name} | Invoke-Expression", err=True)
            click.echo(f"# PowerShell (legacy): tos cd {env_name} | Invoke-Expression", err=True)
        else:
            click.echo(f"cd /d {path}")
            click.echo(f"\n# CMD: td {env_name}", err=True)
            click.echo(f"# CMD (legacy): tos cd {env_name} | cmd", err=True)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument('env_name')
def path(env_name):
    """Print only the resolved path for an env name.

    Intended for shell wrappers to consume. Writes the path to stdout
    and no extra text. On error, prints a message to stderr and exits non-zero.
    """
    try:
        env_vars = load_env_config()

        match_key = _resolve_env_key_case_insensitive(env_vars, env_name)
        if not match_key:
            click.echo(f"Environment variable '{env_name}' not found", err=True)
            sys.exit(1)

        path_value = env_vars[match_key]
        click.echo(path_value)
    except Exception as e:
        click.echo(f"Error resolving path: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--limit', default=None, type=int, help='Number of entries to show (overrides config)')
@click.option('--command', default=None, help='Filter by command name')
def history(limit, command):
    """Show command execution history."""
    try:
        db_file = get_db_file()
        
        if not db_file.exists():
            click.echo("No history available yet.")
            return
        
        # Load limit from config if not provided
        if limit is None:
            config = load_config_toml()
            limit = config.get('history_limit', 100)
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT timestamp, command, arguments, working_directory, status FROM command_history"
        params = []
        
        if command:
            query += " WHERE command = ?"
            params.append(command)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            if command:
                click.echo(f"No history found for command: {command}")
            else:
                click.echo("No history available yet.")
            return
        
        click.echo(f"\n{'Timestamp':<20} {'Command':<15} {'Arguments':<30} {'Status':<10} {'Directory'}")
        click.echo("=" * 120)
        
        for row in rows:
            timestamp, cmd, args, working_dir, status = row
            # Format timestamp
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            
            # Truncate long arguments and directory
            args_display = (args[:27] + '...') if len(args) > 30 else args
            dir_display = working_dir
            
            status_icon = '✓' if status == 'success' else '✗'
            
            click.echo(f"{time_str:<20} {cmd:<15} {args_display:<30} {status_icon:<10} {dir_display}")
        
        # Show summary
        click.echo("=" * 120)
        click.echo(f"Showing {len(rows)} most recent entries (limit: {limit})")
        
        if command:
            click.echo(f"Filtered by command: {command}")
        
    except Exception as e:
        click.echo(f"Error reading history: {e}", err=True)


if __name__ == "__main__":
    cli(windows_expand_args=False)
