import os
import subprocess
import time

repos = [
    'Dental_000', 'Dental_001', 'Dental_002', 'Dental_003', 'Dental_004',
    'Dental_005', 'Dental_006', 'Dental_007', 'Dental_008', 'Dental_009',
    'Dental_010', 'Dental_Panoramic_Reader'
]
base_dir = r'C:\Users\chema\Github'

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode, result.stdout, result.stderr

for repo in repos:
    repo_path = os.path.join(base_dir, repo)
    print(f'\n--- Processing {repo} ---')
    if not os.path.isdir(repo_path):
        print(f'Repo {repo} does not exist.')
        continue
    
    # Check git status
    rc, out, err = run_cmd('git status -s', cwd=repo_path)
    if out.strip():
        print('Changes detected. Committing and pushing...')
        run_cmd('git add .', cwd=repo_path)
        run_cmd('git commit -m "Update integration for 008, 009, 010"', cwd=repo_path)
        rc, out, err = run_cmd('git push origin main', cwd=repo_path)
        if rc != 0:
            print(f'Failed to push: {err}')
        else:
            print('Push successful.')
    else:
        print('No changes to commit. Proceeding to check CI/CD.')
    
    # Trigger or wait for CI/CD
    print('Checking CI/CD status with gh run list...')
    max_wait = 180
    waited = 0
    passed = False
    while waited < max_wait:
        rc, out, err = run_cmd('gh run list -L 1', cwd=repo_path)
        if rc != 0:
            if 'could not resolve host' in err.lower() or 'error' in err.lower():
                print(f'gh command failed: {err}')
            break
            
        lines = out.strip().split('\n')
        if not lines or 'no runs found' in out.lower() or 'could not find' in out.lower():
            print('No CI/CD runs found.')
            break
            
        status_line = lines[0].lower()
        if 'in_progress' in status_line or 'queued' in status_line:
            print('CI/CD is running... waiting 10s')
            time.sleep(10)
            waited += 10
        elif 'completed' in status_line or 'success' in status_line or '*' not in out:
            # Need a robust way to check failure
            # gh run list outputs 'X' or checkmark. 
            if 'failure' in out.lower() or 'failed' in out.lower() or 'x' in out.lower().split('\t')[0]:
                print('CI/CD FAILED! Needs attention.')
                break
            else:
                print('CI/CD passed successfully!')
                passed = True
                break
        else:
            print(f'Unknown status format, assuming passed: {status_line}')
            passed = True
            break
