from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .serializers import NewsSerializer
from news.models import News, Category
from .permissions import IsAdminOrReadOnly


class NewsAPISetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = NewsAPISetPagination

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            return Response({'category' : category.name})
        except (ObjectDoesNotExist, ValueError):
            return Response({'error': 'category with this pk does not exist'})
