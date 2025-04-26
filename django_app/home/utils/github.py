import requests
import base64
from urllib.parse import urlparse 
import uuid
from .ai_agent import analyze_code_with_llm


def get_owner_url(url):
    passed_url = urlparse(url)
    part_path = passed_url.path.strip("/").split("/")
    if len(part_path) >= 2:
        owner , repo = part_path[0] , part_path[1]
        return owner , repo
    return None , None


def fetch_url_files(repo_url ,pr_number ,  github_token = None):
    owner , repo = get_owner_url(repo_url)
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {"authorization" : f"{github_token}"} if github_token else {}
    response = requests.get(url , headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_file_content(repo_url , filepath ,  github_token = None):
    owner , repo = get_owner_url(repo_url)
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}"
    headers = {"authorization" : f"{github_token}"} if github_token else {}
    response = requests.get(url , headers=headers)
    response.raise_for_status()
    content = requests.json()
    return base64.b64decode(content['content']).decode()
    


def analyze_pr(repo_url,pr_number,github_token = None):
    task_id = str(uuid.uuid4())
    try:
        pr_files = fetch_url_files(repo_url , pr_number , github_token= None)
        analysis_results = []
        for file in pr_files:
            file_name  = file['file_name']
            raw_content = fetch_file_content(repo_url , file_name , github_token)
            analysis_result  = analyze_code_with_llm(raw_content , file_name)  
            analysis_results.append ({"results": analysis_result , "file_name" : file_name})
            return {"task_id" : task_id , "results": analysis_result , "file_name" : file_name}
    except Exception as e:
        print(e)
        return {"task_id": task_id , "result": []}  
    