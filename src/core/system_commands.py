# system_commands.py

import subprocess

def run_command(command):
    """Execute a system command and return the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.decode('utf-8')}"

def list_directory(path):
    """List the contents of a directory."""
    command = f"ls {path}"
    return run_command(command)

def get_system_info():
    """Get basic system information."""
    command = "uname -a"
    return run_command(command)

def check_service_status(service_name):
    """Check the status of a system service."""
    command = f"brew services list | grep {service_name}"
    return run_command(command)