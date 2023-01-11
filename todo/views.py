import random
from copy import deepcopy

from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from todo.models import Todo
from todo.serializers import TodoSerializer
from todo.swagger import apidocs

@method_decorator(name='list', decorator=swagger_auto_schema(**apidocs.TODO_LIST_VIEW))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(**apidocs.TODO_RETRIEVE_VIEW))
@method_decorator(name='destroy', decorator=swagger_auto_schema(**apidocs.TODO_DESTROY_VIEW))
class TodoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer

    def get_queryset(self):
        """
        Return a list of all the Todo objects
        for the currently authenticated user.
        """
        user = self.request.user
        return Todo.objects.filter(creator_id=user.id)

    @swagger_auto_schema(**apidocs.TODO_CREATE_VIEW)
    def create(self, request):
        data = deepcopy(request.data)
        data.update({"creator_id": self.request.user.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(**apidocs.TODO_RETRIEVE_RANDOM_VIEW)
    @action(detail=False, methods=['get'])
    def random(self, request):
        todo_objs = list(self.get_queryset())
        if todo_objs:
            random_todo_obj = random.choice(todo_objs)
            serializer = self.get_serializer(random_todo_obj)
            data = serializer.data
        else:
            data = []
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**apidocs.TODO_UPDATE_VIEW)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(**apidocs.TODO_PARTIAL_UPDATE_VIEW)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
