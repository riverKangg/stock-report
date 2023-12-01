import subprocess
from datetime import datetime

def get_root_directory():
    result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE, text=True)
    root_dir = result.stdout.strip()
    return root_dir

def get_formmated_date():
    formatted_date = datetime.now().strftime('%Y-%m-%d')
    return formatted_date
