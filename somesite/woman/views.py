from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратна связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
        ]


def index(request):
    posts = Woman.objects.all()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,

    }
    return render(request, 'woman/index.html', context=context)


def about(request):
    return render(request, 'woman/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>');


def show_post(request, post_slug):
    post = get_object_or_404(Woman, slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }
    return render(request, 'woman/post.html', context=context)


def show_category(request, cat_id):
    posts = Woman.objects.filter(cat_id=cat_id)

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Отображение по категориям',
        'cat_selected': cat_id,

    }
    return render(request, 'woman/index.html', context=context)
