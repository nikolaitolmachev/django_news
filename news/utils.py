MENU = [
    {'title': 'О сайте', 'url_name' : 'about'},
    {'title': 'Добавить статью', 'url_name' : 'add_page'},
    {'title': 'API', 'url_name' : 'api-list'},
]

class DataMixin:
    paginate_by = 5
    title_page = None
    category_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page != None:
            self.extra_context['title'] = self.title_page

        if self.category_selected != None:
            self.extra_context['category_selected'] = self.category_selected

    def get_mixin_context(self, context, **kwargs):
        context['category_selected'] = None
        context.update(kwargs)
        return context