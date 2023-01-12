from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    creator_id = serializers.IntegerField()

    class Meta:
        model = Todo
        exclude = ['creator']

class TodoQueryParamSerializer(serializers.Serializer):
    completed = serializers.BooleanField(required=False, allow_null=True)
