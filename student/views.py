


from django.shortcuts import render
from django.http import HttpResponse


def student_list(request):
    return HttpResponse("Page de la liste des étudiants")


def add_student(request):
    return HttpResponse("Page d'ajout d'un étudiant")