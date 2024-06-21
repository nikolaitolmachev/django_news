from django import forms
from .models import News, Category
from django.core.validators import ValidationError


class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории',
                                      empty_label='Категория не выбрана')

    class Meta:
        model = News
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'category', 'tags']  #'__all__'
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'row': 5}),
        }
        labels = {'slug' : 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов.')
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')