import subprocess
import os
from collections import defaultdict

def get_changed_files(repo_path='.', base_branch='main'):
    os.chdir(repo_path)
    current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                    capture_output=True, text=True).stdout.strip()
    result = subprocess.run(['git', 'diff', '--name-status', f'{base_branch}...{current_branch}'], 
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return []

    changed_files = []
    for line in result.stdout.split('\n'):
        if line:
            status, file_path = line[0], line[2:]
            changed_files.append((status, file_path))

    return changed_files, current_branch

def get_file_changes(file_path):
    result = subprocess.run(['git', 'diff', 'HEAD', file_path], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout

def analyze_changes(changed_files):
    changes = defaultdict(list)
    for status, file_path in changed_files:
        if status == 'M':
            file_diff = get_file_changes(file_path)
            if file_diff:
                additions = len([line for line in file_diff.split('\n') if line.startswith('+')])
                deletions = len([line for line in file_diff.split('\n') if line.startswith('-')])
                changes['modified'].append((file_path, additions, deletions))
        elif status == 'A':
            changes['added'].append(file_path)
        elif status == 'D':
            changes['deleted'].append(file_path)
        elif status == 'R':
            changes['renamed'].append(file_path)
    return changes

def generate_commit_message(changes, current_branch):
    lines = [f"Update branch '{current_branch}'", ""]

    if changes['added']:
        lines.append("Added:")
        for file in changes['added']:
            lines.append(f"- {file}")
        lines.append("")

    if changes['deleted']:
        lines.append("Deleted:")
        for file in changes['deleted']:
            lines.append(f"- {file}")
        lines.append("")

    if changes['modified']:
        lines.append("Modified:")
        for file, additions, deletions in changes['modified']:
            lines.append(f"- {file} (+{additions}, -{deletions})")
        lines.append("")

    if changes['renamed']:
        lines.append("Renamed:")
        for file in changes['renamed']:
            lines.append(f"- {file}")
        lines.append("")

    return "\n".join(lines)

def main():
    repo_path = input("Enter the path to the Git repository (press Enter for current directory): ").strip() or '.'
    base_branch = input("Enter the name of the base branch (press Enter for 'main'): ").strip() or 'main'

    changed_files, current_branch = get_changed_files(repo_path, base_branch)
    
    if changed_files:
        print(f"\nFiles changed between '{base_branch}' and '{current_branch}':")
        for status, file_path in changed_files:
            status_desc = {
                'M': 'Modified',
                'A': 'Added',
                'D': 'Deleted',
                'R': 'Renamed',
                'C': 'Copied',
            }.get(status, 'Unknown')
            print(f"{status_desc}: {file_path}")

        changes = analyze_changes(changed_files)
        commit_message = generate_commit_message(changes, current_branch)
        
        print("\nGenerated Commit Message:")
        print("-------------------------")
        print(commit_message)
    else:
        print(f"No changes found between '{base_branch}' and '{current_branch}'.")

if __name__ == "__main__":
    main()