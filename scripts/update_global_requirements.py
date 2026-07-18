import os
import glob

def update_requirements():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dental_core_req = "git+https://github.com/HyunchanAn/Dental_Core.git@master\n"
    
    # Search for all requirements.txt in Dental_001 ~ Dental_014
    for i in range(1, 15):
        repo_name = f"Dental_{i:03d}"
        req_path = os.path.join(base_dir, repo_name, "requirements.txt")
        
        if os.path.exists(req_path):
            with open(req_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            # Check if dental_core is already there
            has_core = any("Dental_Core.git" in line for line in lines)
            
            # Remove any local submodule references (-e ./modules/Dental_Core etc)
            cleaned_lines = [line for line in lines if "Dental_Core" not in line or "github.com" in line]
            
            if not has_core:
                cleaned_lines.append(dental_core_req)
                with open(req_path, "w", encoding="utf-8") as f:
                    f.writelines(cleaned_lines)
                print(f"Updated: {req_path}")
            else:
                print(f"Skipped (already has core): {req_path}")
        else:
            # Create if doesn't exist
            print(f"Created: {req_path}")
            with open(req_path, "w", encoding="utf-8") as f:
                f.write(dental_core_req)

if __name__ == "__main__":
    update_requirements()
