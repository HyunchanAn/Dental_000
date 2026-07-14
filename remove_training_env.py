import os
import re

repos_to_fix = [
    'Dental_000', 'Dental_006', 'Dental_007', 'Dental_011', 'Dental_Panoramic_Reader'
]
base_dir = r'C:\Users\chema\Github'
training_env_text = "> **[학습 환경 사양]** 실질적 모델 학습은 **RTX 5080 + 라이젠9-6 9900x** 환경에서 진행되었습니다.\n"
training_env_text2 = "## 학습 환경 (Training Environment)\n" + training_env_text

def fix_readme(repo_name):
    repo_path = os.path.join(base_dir, repo_name)
    readme_path = os.path.join(repo_path, "README.md")
    
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove the exact string if present
        if training_env_text2 in content:
            content = content.replace(training_env_text2, "")
        if training_env_text in content:
            content = content.replace(training_env_text, "")
            
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[{repo_name}] Fixed README.")

if __name__ == "__main__":
    for repo in repos_to_fix:
        fix_readme(repo)
