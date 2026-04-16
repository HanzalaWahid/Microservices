import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx

app = FastAPI()

DJANGO_BASE_URL = os.environ.get("DJANGO_BASE_URL", "http://127.0.0.1:8002")

class AnalysePRRequest(BaseModel):
    repo_url: Optional[str] = None
    pr_number: Optional[int] = None
    repo_owner: Optional[str] = None
    repo_name: Optional[str] = None
    pull_number: Optional[int] = None
    github_token: Optional[str] = None

@app.post("/start_task")
async def start_end_point(task_request: AnalysePRRequest):
    if task_request.repo_url and task_request.pr_number is not None:
        pr_url = f"{task_request.repo_url}/pull/{task_request.pr_number}"
    elif (
        task_request.repo_owner
        and task_request.repo_name
        and task_request.pull_number is not None
    ):
        pr_url = f"https://github.com/{task_request.repo_owner}/{task_request.repo_name}/pull/{task_request.pull_number}"
    else:
        raise HTTPException(
            status_code=422,
            detail=(
                "Provide either repo_url and pr_number, "
                "or repo_owner, repo_name, and pull_number."
            ),
        )

    data = {
        "pr_url": pr_url,
        "github_token": task_request.github_token,
    }

    target_url = f"{DJANGO_BASE_URL.rstrip('/')}/start_task/"
    print(f"Forwarding to Django: {target_url}")
    print(f"Payload: {data}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                target_url,
                json=data,
                timeout=30,
                follow_redirects=False,
            )
        except httpx.RequestError as exc:
            return {
                "error": "fail to start task",
                "details": f"Request to Django failed: {exc}",
            }

        if response.status_code != 200:
            details = None
            try:
                details = response.json()
            except ValueError:
                details = response.text
            return {
                "error": "fail to start task",
                "status_code": response.status_code,
                "location": response.headers.get("location"),
                "details": details,
            }

    result_json = None
    try:
        result_json = response.json()
    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="Django returned invalid JSON for task creation",
        )

    task_id = result_json.get("task_id")
    if not task_id:
        raise HTTPException(
            status_code=502,
            detail={
                "error": "Django did not return task_id",
                "response": result_json,
            },
        )

    return {"task_id": task_id, "status": "Task started"}


@app.get("/task_status/{task_id}/")
async def task_status_endpoint(task_id : str):
    async with httpx.AsyncClient() as client:
        response  = await client.get(
            f"http://127.0.0.1:8000/task_status_view/{task_id}/",

        )
        

        return response.json()
    return {"message": "Something went worng"}

from fastapi import FastAPI ,status
from pydantic import BaseModel
from typing import Optional
import httpx

app = FastAPI()

class Analyse_PR_Request(BaseModel):
    repo_url : str
    pr_number : int
    github_token : Optional[str] = None

@app.post("/start_task")
async def start_end_point(task_request: Analyse_PR_Request):
    data ={
    "repo_url" : task_request.repo_url,
    "pr_number": task_request.pr_number,
    "github_token": task_request.github_token,
    }

    async with httpx.AsyncClient as client:
        response = await client.post(
            "http://127.0.0.1:8000/start_task/",
            data = data 
        )
        if response.status_code != 200:
            return {"error ": "fail to start task "  , "details": response.text}  

    print(data)
    task_id = response.json.get('task_id')
    return {"task_id": task_id  , "status": "Task started"}


@app.get("/task_status/{task_id}/")
async def task_status_endpoint(task_id : str):
    async with  httpx.Client as client:
        response  = await client.get(
            f"http://127.0.0.1:8000/tasK_status_view/{task_id}",

        )
        

        return response.json()
    return {"message": "Something went worng"}