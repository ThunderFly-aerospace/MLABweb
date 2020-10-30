from django.http import HttpResponse
from pymongo import MongoClient
from github import Github
from django.shortcuts import render
from django.conf import settings

def update_record(repository):
    g = Github(settings.GITHUB_TOKEN)

    mdb = MongoClient().OpenCat
    repository = list(mdb.repositories.find({'_id': repository}))

    if repository == []:
        print("tento zaznam jeste nemam v DB")
        g.get_repo(repository)
        print(g)

    else:
        repository = repository[0]
        print("mam v DB")
        print(repository)

    return repository


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def module(request, org, name):
    full_name = '{}/{}'.format(org, name)

    mdb = MongoClient().OpenCat
    repository = list(mdb.repositories.find({'_id': full_name}))

    if repository == []:
        return HttpResponse("This modul doesnot exists")

    data = update_record(full_name)


    return render(request, 'module.html', data)
