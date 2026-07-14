import subprocess, os
repos = ['Dental_000', 'Dental_006', 'Dental_007', 'Dental_011', 'Dental_Panoramic_Reader']
for r in repos:
    p = os.path.join(r'C:\Users\chema\Github', r)
    subprocess.run('git add README.md', shell=True, cwd=p)
    subprocess.run('git commit -m "docs: remove training hardware spec from non-model repos"', shell=True, cwd=p)
    subprocess.run('git push origin HEAD', shell=True, cwd=p)
