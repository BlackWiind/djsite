from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from .models import *

menu = ["О сайте", "Добаыить статью", "Обратна связь"]


def index(request):
    posts = Woman.objects.all()
    return render(request, 'woman/index.html', {'posts': posts,
                                                'menu': menu,
                                                'title': 'Главная страница'})


def about(request):
    return render(request, 'woman/about.html', {'menu': menu, 'title': 'О сайте'})


def categories(request, catid):
    if request.GET:
        print(request.GET)

    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}<p>");


def archive(request, year):
    if int(year) > 2021:
        return redirect('home', permanent=False);
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}<p>");


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не нацдена</h1>');