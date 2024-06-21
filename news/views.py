from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import News, TagPost
from .forms import AddPostForm
from .utils import DataMixin


class NewsHome(DataMixin, ListView):
    #model = News
    template_name = 'news/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    category_selected = 0

    def get_queryset(self):
        return News.published.all().select_related('category')


def about(request):
    return render(request, 'news/about.html', {'title': 'О сайте'})


class ShowPost(DataMixin, DetailView):
    template_name = 'news/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(News.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'news/addpage.html'
    title_page = 'Добавление новости'
    permission_required = 'news.add_news'

    def form_valid(self, form):
        n = form.save(commit=False)
        n.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = News
    fields = ['title', 'content', 'photo', 'is_published', 'category']
    template_name = 'news/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование новости'
    permission_required = 'news.change_news'


class NewsCategory(DataMixin, ListView):
    template_name = 'news/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return News.published.filter(category__slug=self.kwargs['cat_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].category

        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      category_selected=cat.pk)


class NewsTags(DataMixin, ListView):
    template_name = 'news/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return News.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])

        return self.get_mixin_context(context,
                                      title='Тег - ' + tag.tag,
                                      category_selected=None)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')