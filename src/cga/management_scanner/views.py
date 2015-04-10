import os
import json
import shutil
from django.shortcuts import render
from django.http import HttpResponse
from scaner.models import FileSystem, Events
from datetime import datetime, timedelta


def index(request):
    return render(request, 'base.html')


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


def all_previous_version(document):
    documents = [document]
    while document.previous_version:
        document = document.previous_version
        documents.append(document)
    return documents


def del_all_next_versions(need_file, last_file):
    while last_file.version > need_file.version:
        last_file.delete()
        last_file = FileSystem.objects(key_for_all_versions=need_file.key_for_all_versions).order_by("-version").first()


def get_files(request):
    if request.body:
        document_from_ui = json.loads(request.body)
        document = FileSystem.objects(id=document_from_ui["id"]).first()
        documents = all_previous_version(document)
    else:
        documents = FileSystem.objects(path_name__startswith="/home/", has_next=False)
    return send_files(documents)


def api_logs(request):
    date_event = json.loads(request.body)
    date_from = datetime.strptime(date_event['from'][:18], "%Y-%m-%dT%H:%M:%S")
    date_to = datetime.strptime(date_event['to'][:18], "%Y-%m-%dT%H:%M:%S")
    date_to += timedelta(days=1)
    logs = Events.objects.filter(date__lte=date_to, date__gte=date_from)
    return send_files(logs)


def downgrade(request):
    data_file = json.loads(request.body)
    need_file = FileSystem.objects(id=data_file['this_id']).first()
    key_for_versions = need_file.key_for_all_versions
    last_file = FileSystem.objects(key_for_all_versions=key_for_versions).order_by("-version").first()
    last_file.disabled = True
    last_file.save()
    if need_file:
        if need_file.hash_sum != last_file.hash_sum:
            while not need_file.body:
                need_file = need_file.previous_version
            with open(last_file.path_name, 'w') as this_file:
                this_file.write(need_file.body.read())
        if need_file.permissions != last_file.permissions:
            os.chmod(last_file.path_name, int(str(need_file.permissions), 8))
        if need_file.path_name != last_file.path_name:
            shutil.move(last_file.path_name, need_file.path_name)
        del_all_next_versions(need_file, last_file)
        documents = all_previous_version(need_file)
        need_file.has_next = False
        need_file.save()
        return send_files(documents)
    return HttpResponse()