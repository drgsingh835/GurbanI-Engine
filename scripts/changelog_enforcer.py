import sys
import subprocess
import os

# Define files/directories that require a changelog update when modified
CODE_EXTENSIONS = ('.py', '.js', '.json', '.md', '.yml', '.yaml', '.sh', '.bat')
IGNORE_PATTERNS = ('CHANGELOG.md', 'task.md', 'implementation_plan.md', 'walkthrough.md')

def get_staged_files():
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception as e:
        print(f"[-] Failed to get staged files: {e}")
        return []

def install_hook():
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_dir = os.path.join(workspace_dir, '.git')
    
    if not os.path.exists(git_dir):
        print("[-] Error: Not a git repository or run from the wrong directory.")
        sys.exit(1)
        
    hooks_dir = os.path.join(git_dir, 'hooks')
    os.makedirs(hooks_dir, exist_ok=True)
    
    pre_commit_hook = os.path.join(hooks_dir, 'pre-commit')
    
    hook_content = """#!/bin/sh
# Changelog Enforcer Git Hook
# Automatically installed by scripts/changelog_enforcer.py

python scripts/changelog_enforcer.py
"""
    
    with open(pre_commit_hook, 'w', newline='\n') as f:
        f.write(hook_content)
        
    # Make executable on Unix-like environments (harmless on Windows)
    try:
        os.chmod(pre_commit_hook, 0o755)
    except Exception:
        pass
        
    print("[+] Git pre-commit hook installed successfully at:")
    print(f"    {pre_commit_hook}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--install':
        install_hook()
        sys.exit(0)

    staged_files = get_staged_files()
    
    if not staged_files:
        sys.exit(0)

    # Check if CHANGELOG.md is staged
    changelog_updated = any(os.path.basename(f) == 'CHANGELOG.md' for f in staged_files)
    
    if changelog_updated:
        print("[+] Changelog update verified.")
        sys.exit(0)

    # Determine if any of the staged changes require a changelog entry
    requires_changelog = False
    affected_files = []
    
    for f in staged_files:
        basename = os.path.basename(f)
        if basename in IGNORE_PATTERNS:
            continue
        if f.endswith(CODE_EXTENSIONS):
            requires_changelog = True
            affected_files.append(f)
            
    if requires_changelog:
        print("====================================================")
        print(" [!] CHANGELOG ENFORCEMENT ERROR")
        print("====================================================")
        print("You have staged changes to code/config files, but 'CHANGELOG.md' has not been updated.")
        print("\nAffected files:")
        for af in affected_files[:5]:
            print(f"  - {af}")
        if len(affected_files) > 5:
            print(f"  - ... and {len(affected_files) - 5} more")
            
        print("\nFix Action:")
        print("  Please update the 'CHANGELOG.md' with details about your new feature(s) or bug fix(es) and stage it before committing.")
        print("\nTo bypass (for trivial or documentation-only commits):")
        print("  git commit --no-verify")
        print("====================================================")
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
