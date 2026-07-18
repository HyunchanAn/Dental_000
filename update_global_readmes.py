import os

repos = [
    'Dental_000', 'Dental_001', 'Dental_002', 'Dental_003', 'Dental_004',
    'Dental_005', 'Dental_006', 'Dental_007', 'Dental_008', 'Dental_009',
    'Dental_010', 'Dental_011', 'Dental_012', 'Dental_013', 'Dental_Panoramic_Reader'
]
base_dir = r'C:\Users\chema\Github'

badges = "![Status](https://img.shields.io/badge/Status-v1.0%20Release-brightgreen) ![Python](https://img.shields.io/badge/Python-3.12%2B-blue) ![Backend](https://img.shields.io/badge/Backend-YOLOv8-red) ![UI](https://img.shields.io/badge/UI-Streamlit-orange) ![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD%20Pipeline-passing-brightgreen?logo=github)"
training_env_text = "> **[학습 환경 사양]** 실질적 모델 학습은 **RTX 5080 + 라이젠9-6 9900x** 환경에서 진행되었습니다.\n"

def update_readme(repo_name):
    repo_path = os.path.join(base_dir, repo_name)
    readme_path = os.path.join(repo_path, "README.md")
    
    if not os.path.exists(readme_path):
        print(f"[{repo_name}] No README.md found, creating one.")
        content = f"# {repo_name}\n\n## 1. 개요\n\n## 2. 설치 및 실행 방법\n"
    else:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

    lines = content.split('\n')
    
    # 1. Update Badges
    has_status_badge = False
    for i, line in enumerate(lines):
        if "![Status]" in line or "![Python]" in line or "![Backend]" in line or "![Hugging Face]" in line:
            # If multiple badges are on the same line, replace the entire line
            lines[i] = badges
            has_status_badge = True
            break
            
    if not has_status_badge:
        lines.insert(0, badges + "\n")
        
    content = '\n'.join(lines)
    
    # 2. Add Training Environment
    if "RTX 5080" not in content:
        if "## 학습 환경" in content:
            content = content.replace("## 학습 환경", "## 학습 환경\n" + training_env_text)
        elif "## 1. 개요" in content:
            content = content.replace("## 1. 개요", "## 1. 개요\n" + training_env_text)
        elif "## 개요" in content:
            content = content.replace("## 개요", "## 개요\n" + training_env_text)
        else:
            content += "\n## 학습 환경 (Training Environment)\n" + training_env_text
            
    # 3. Ensure Overview & Install Instructions exist
    if "개요" not in content:
        content += "\n## 개요\n이 레포지토리는 치과 AI 모듈러 시스템의 일부입니다.\n"
    if "설치 및 실행 방법" not in content:
        content += "\n## 설치 및 실행 방법\n```bash\npip install -r requirements.txt\n```\n"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[{repo_name}] README.md updated successfully.")

if __name__ == "__main__":
    for repo in repos:
        update_readme(repo)
