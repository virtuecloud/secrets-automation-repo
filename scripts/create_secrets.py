import os
import base64
from github import Github, Auth

# ✅ Fetch environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Personal Access Token (PAT)
GITHUB_OWNER = os.getenv("GITHUB_OWNER")  # GitHub username or organization name
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")  # Full repo name (org/repo or user/repo)

# ✅ Ensure required environment variables are set
if not GITHUB_TOKEN or not GITHUB_OWNER or not GITHUB_REPOSITORY:
    raise ValueError("❌ Missing environment variables! Ensure GITHUB_TOKEN, GITHUB_OWNER, and GITHUB_REPOSITORY are set.")

# ✅ Extract only the repository name (to avoid issues with org/user prefixes)
repo_name = GITHUB_REPOSITORY.split("/")[-1]

# ✅ Authenticate using PAT
auth = Auth.Token(GITHUB_TOKEN)
github_client = Github(auth=auth)

try:
    # 🔹 Fetch repository
    print(f"🔹 Fetching repository: {GITHUB_OWNER}/{repo_name} ...")
    repo = github_client.get_repo(f"{GITHUB_OWNER}/{repo_name}")

    # 🔹 Define secrets
    secrets = {
        "SECRET_1": "value1",
        "SECRET_2": "value2",
        "SECRET_3": "value3",
    }

    # 🔹 Create secrets in GitHub (must be base64-encoded)
    for secret_name, secret_value in secrets.items():
        encoded_value = base64.b64encode(secret_value.encode()).decode()  # Encode in base64
        repo.create_secret(secret_name, encoded_value)
        print(f"✅ Secret '{secret_name}' added to {repo_name}")

except Exception as e:
    print(f"❌ Error creating secrets in {repo_name}: {e}")

finally:
    github_client.close()  # Close GitHub connection
    print("🔹 GitHub connection closed.")