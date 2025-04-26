from celery import Celery 
from celery import shared_task
from home.utils.github import analyze_pr


app = Celery('django_app')
app.config_from_object('django.cong.settings' , namespace = "Celery")
app.autodiscover_tasks()

@shared_task
def analyze_repo_task(pr_number , repo_url , github_token = None):
    result = analyze_pr(repo_url , pr_number  , github_token)
    return result

