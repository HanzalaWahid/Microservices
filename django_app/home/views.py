from rest_framework.decorators import api_view
from rest_framework.response import Response
from .task import analyze_repo_task
from celery.result import AsyncResult

# Create your views here.

@api_view(['POST'])
def start_task(request):
    data = request.data
<<<<<<< HEAD
    repo_url = data.get('repo_url')
    pr_number = data.get('pr_number')
    github_token = data.get('github_token')
    task = analyze_repo_task.delay(repo_url , pr_number ,github_token)

    return Response({"task_id": task.id ,
                    "status": "Task_started"     })
=======
    pr_url = data.get('pr_url')
    github_token = data.get('github_token')

    if not pr_url:
        return Response(
            {"error": "pr_url is required"},
            status=400,
        )

    task = analyze_repo_task.delay(pr_url, github_token)
    return Response({"task_id": task.id, "status": "Task_started"})
>>>>>>> 47a610d (Initial commit - microservices project)

@api_view(['GET'])
def task_status_view(request , task_id):
    result =  AsyncResult(task_id)
    response = ({
        "task_id" : task_id,
        "status" : result.state,
        "result" : result.result
    })

    return Response(response)