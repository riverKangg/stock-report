import subprocess


def get_git_root_directory():
    result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()