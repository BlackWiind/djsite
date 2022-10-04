from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .models import *
from .serializers import WomanSerializer
from .utils import *


class WomanHome(DataMixin, ListView):
    model = Woman
    template_name = 'woman/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Woman.objects.filter(is_published=True).select_related('cat')


def about(request):
    return render(request, 'woman/about.html', {'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin,  DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'woman/addpage.html'
    login_url = '/admin/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'woman/contact.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>');


class ShowPost(DataMixin, DetailView):
    model = Woman
    template_name = 'woman/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str(context['post'].title))
        return dict(list(context.items()) + list(c_def.items()))



class WomanCategory(DataMixin, ListView):
    model = Woman
    template_name = 'woman/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Woman.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'woman/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'woman/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class WomanAPIView(APIView):
    def get(self, request):
        queryset = Woman.objects.all()
        return Response({'posts': WomanSerializer(queryset, many=True).data})

    def post(self, request):
        serializer = WomanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_post = Woman.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id'],
        )

        return Response({'post': WomanSerializer(new_post).data})