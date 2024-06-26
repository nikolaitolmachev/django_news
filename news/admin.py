from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import News, Category, Comment

#admin.site.register(News, NewsAdmin)
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'category', 'tags'] # display in change mode of post

    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug' : ('title', )} # for auto slug

    filter_horizontal =  ['tags'] # horizontal editor for 'tags'

    list_display = ('title', 'post_photo', 'time_created', 'is_published', 'category')
    list_display_links = ('title', )
    ordering = ['time_created', 'title']
    list_editable = ('is_published', )
    list_per_page = 10

    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'category__name']
    list_filter = ['category__name', 'is_published']

    save_on_top = True

    @admin.display(description='Фото', ordering='content')
    def post_photo(self, news: News):
        if news.photo:
            return mark_safe(f'<img src="{news.photo.url}" width="50" />')
        else:
            return 'Без фото'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f'Изменено {count} записей.')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f'{count} записей снято с публикации!', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ['name']


class PostInline(admin.TabularInline):
    model = News.comments.through


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    inlines = [
        PostInline,
    ]