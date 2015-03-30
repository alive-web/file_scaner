from django.shortcuts import render
from scaner.models import FileSystem


def index(request):
    documents = FileSystem.objects(path_name__startswith="/home/", has_next=False)
    context = {"documents": documents}
    return render(request, 'index.html', context)
