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