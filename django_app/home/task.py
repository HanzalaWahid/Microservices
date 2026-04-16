from celery import Celery 
from celery import shared_task
from home.utils.github import analyze_pr


app = Celery('django_app')
<<<<<<< HEAD
app.config_from_object('django.cong.settings' , namespace = "Celery")
app.autodiscover_tasks()

@shared_task
def analyze_repo_task(pr_number , repo_url , github_token = None):
    result = analyze_pr(repo_url , pr_number  , github_token)
=======
app.config_from_object('django.conf.settings' , namespace = "Celery")
app.autodiscover_tasks()

@shared_task
def analyze_repo_task(pr_url, github_token=None):
    result = analyze_pr(pr_url, github_token)
>>>>>>> 47a610d (Initial commit - microservices project)
    return result

