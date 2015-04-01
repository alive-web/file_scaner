import json
from django.shortcuts import render
from django.http import HttpResponse
from scaner.models import FileSystem, Events


def send_files(documents):
    files = []
    for document in documents:
        data = {
            'path_name': document.path_name,
            'date': str(document.date),
        }
        if hasattr(document, "is_dir"):
            data["is_dir"] = document.is_dir
        if hasattr(document, "event"):
            data["event"] = document.event
        files.append(data)
    return HttpResponse(json.dumps(files), content_type="application/json")


def index(request):
    return render(request, 'base.html')


def get_files(request):
    documents = FileSystem.objects(path_name__startswith="/home/", has_next=False)
    return send_files(documents)


def api_logs(request):
    logs = Events.objects()
    if request.body:
        data1 = json.loads(request.body)
    return send_files(logs)