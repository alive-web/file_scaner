import json
from django.shortcuts import render
from django.http import HttpResponse
from scaner.models import FileSystem, Events
from datetime import datetime


def send_files(documents):
    files = []
    for document in documents:
        data = {
            'path_name': document.path_name,
            'date': str(document.date),
            'id': str(document.id)
        }
        if hasattr(document, "is_dir"):
            data["is_dir"] = document.is_dir
        if hasattr(document, "event"):
            data["event"] = document.event
        if hasattr(document, "version"):
            data["version"] = document.version
        if hasattr(document, "parent"):
            data["parent"] = str(document.parent)
        files.append(data)
    return HttpResponse(json.dumps(files), content_type="application/json")


def index(request):
    return render(request, 'base.html')


def get_files(request):
    documents = []
    if request.body:
        document_from_ui = json.loads(request.body)
        document = FileSystem.objects(id=document_from_ui["id"]).first()
        documents = [document]
        while document.previous_version:
            document = document.previous_version
            documents.append(document)
    else:
        documents = FileSystem.objects(path_name__startswith="/home/", has_next=False)
    return send_files(documents)


def api_logs(request):
    date_event = json.loads(request.body)
    date_from = datetime.strptime(date_event['from'][:18], "%Y-%m-%dT%H:%M:%S")
    date_to = datetime.strptime(date_event['to'][:18], "%Y-%m-%dT%H:%M:%S")
    logs = Events.objects.filter(date__lte=date_to, date__gte=date_from)
    return send_files(logs)