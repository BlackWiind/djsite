import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from woman.models import Woman


# class WomanModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content


class WomanSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField()


# def encode():
#     model = WomanModel('Angelina Jolie', 'Content: Some content')
#     model_sr = WomanSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{'
#                         b'"title": "Angelina Jolie",'
#                         b'"content": "Content: Some content"}')
#     data = JSONParser().parse(stream)
#     serializers = WomanSerializer(data=data)
#     serializers.is_valid()
#     print(serializers.data)



