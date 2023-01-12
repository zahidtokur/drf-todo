from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    creator_id = serializers.IntegerField()

    class Meta:
        model = Todo
        exclude = ['creator']
