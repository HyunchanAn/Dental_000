import os
import sys
import subprocess
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
from config.paths import resolve_module_dir

repos = {
    'tests_001': 'Dental_001',
    'tests_002': 'Dental_002',
    'tests_003': 'Dental_003',
    'tests_004': 'Dental_004',
    'tests_005': 'Dental_005',
    'tests_006': 'Dental_006',
    'tests_008': 'Dental_008',
    'tests_009_010': 'Dental_010',
    'tests_panoramic_reader': 'Dental_Panoramic_Reader'
}

def run_tests():
    total_passed = True
    for test_folder, repo_name in repos.items():
        if not os.path.isdir(test_folder):
            continue
            
        print(f"\n[{repo_name}] Running E2E tests in {test_folder}...")
        env = os.environ.copy()
        repo_path = str(resolve_module_dir(repo_name))
        
        # Add the repo path to PYTHONPATH so 'src' can be imported
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = repo_path + os.pathsep + env['PYTHONPATH']
        else:
            env['PYTHONPATH'] = repo_path
            
        result = subprocess.run(['pytest', test_folder, '-q'], env=env, cwd=os.getcwd(), text=True)
        if result.returncode != 0:
            print(f"[{repo_name}] Tests failed!")
            total_passed = False
        else:
            print(f"[{repo_name}] Tests passed successfully!")
            
    return total_passed

if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\nAll E2E tests passed successfully across all repositories!")
    else:
        print("\nSome E2E tests failed. Check logs above.")
