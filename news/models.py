from django.db import models
from django.urls import reverse
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth import get_user_model


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug',
                            validators=[
                                MinLengthValidator(5, message='Мнимум 5 символов'),
                                MaxLengthValidator(100, message='Максимум 100 символов'),
                            ])

    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Фото')

    content = models.TextField(blank=True, verbose_name='Текст новости')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=False, verbose_name='Статус')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)
    comments = models.ManyToManyField('Comment', blank=True, related_name='comments', verbose_name='Комментарии')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return f'{self.title} : {self.content[0:21]}'

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
        ordering = ['-time_created']
        indexes = [
            models.Index(fields=['-time_created'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug' : self.slug})

    #def save(self, *args, **kwargs):
    #    self.slug = slugify(translit_to_eng(self.title))
    #    super().save(*args, **kwargs)



class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug' : self.slug})

    class Meta:
        ordering = ['name']
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug' : self.slug})


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


class Comment(models.Model):
    content_com = models.TextField(blank=False, null=False, verbose_name='Комментарий')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время написания')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL , related_name='comments', null=True, blank=False)

    def __str__(self):
        return self.content_com

    class Meta:
        ordering = ['content_com']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'