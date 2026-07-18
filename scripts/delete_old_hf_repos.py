from huggingface_hub import HfApi

# The old repos under the live-track organization that we want to delete
OLD_REPOS = [
    "live-track/dental-yolo",
    "live-track/dental-caries",
    "live-track/dental-boneloss",
    "live-track/dental-pano-classifier",
    "live-track/dental-sr",
    "live-track/dental-seg",
    "live-track/dental-age",
    "live-track/dental-periapical",
    "live-track/dental-restoration",
    "live-track/dental-cvm",
    "live-track/dental-unet"
]

def delete_old_repos():
    print("Attempting to delete old 'live-track' repositories...")
    api = HfApi()
    
    success_count = 0
    fail_count = 0
    
    for repo in OLD_REPOS:
        try:
            print(f"Deleting {repo}...")
            api.delete_repo(repo_id=repo, repo_type="model")
            print(f"  -> Successfully deleted {repo}!")
            success_count += 1
        except Exception as e:
            print(f"  -> Failed to delete {repo}. Error: {e}")
            fail_count += 1
            
    print("\n" + "="*40)
    print(f"Deletion Summary: {success_count} succeeded, {fail_count} failed.")
    if fail_count > 0:
        print("Note: If you see '403 Forbidden' or similar errors, it means your 'chemahc94' token ")
        print("does not have admin/write access to the 'live-track' organization. In that case, ")
        print("you must ask the Live-track colleague to delete them manually.")
    else:
        print("All old repos were successfully deleted by you!")

if __name__ == "__main__":
    confirm = input("WARNING: Have you fully completed the 'recover_and_export.py' migration? (y/n): ")
    if confirm.lower() == 'y':
        delete_old_repos()
    else:
        print("Deletion aborted. Please finish the migration first!")
