from django import template
from news.models import Category, TagPost
from django.db.models import Count
from news.utils import MENU

register = template.Library()

@register.simple_tag
def get_menu():
    return MENU

@register.inclusion_tag('news/list_categories.html')
def show_categories(category_selected=0):
    categories = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'categories' : categories, 'category_selected': category_selected}

@register.inclusion_tag('news/list_tags.html')
def show_all_tags():
    return {'tags' : TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}