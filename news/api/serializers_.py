from rest_framework import serializers
from .models import News, translit_to_eng

#class NewsModel:
#    def __init__(self, title, content):
#        self.title = title
#        self.content = content


class NewsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_created = serializers.DateTimeField(read_only=True)
    time_updated = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    category_id = serializers.IntegerField()

    def create(self, validated_data):
        news = News.objects.create(**validated_data)
        news.slug = translit_to_eng(news.title.replace(' ', ''))
        news.save()
        return news

    def update(self, instance, validated_data):
        old_title = instance.title
        instance.title = validated_data.get('title', instance.title)
        if old_title != instance.title:
            instance.slug = translit_to_eng(instance.title.replace(' ', ''))

        instance.content = validated_data.get('content', instance.content)
        instance.time_updated = validated_data.get('time_updated', instance.time_updated)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.category_id = validated_data.get('category_id', instance.category_id)

        instance.save()
        return instance


#def encode():
#    model = NewsModel('Angelina Jolie', 'Content: Angelina Jolie')
#    model_sr = NewsSerializer(model)
#    print(model_sr.data, type(model_sr.data), sep='\n')
#    json = JSONRenderer().render(model_sr.data)
#    print(json)
#
#def decode():
#    stream = io.BytesIO(b'{"title" : "Angelina Jolie", "content" : "Content: Angelina Jolie"}')
#    data = JSONParser().parse(stream)
#    serializer = NewsSerializer(data=data)
#    serializer.is_valid()
#    print(serializer.validated_data)