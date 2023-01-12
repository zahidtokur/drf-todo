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
from todo.permissions import IsCreator
from todo.serializers import TodoSerializer, TodoQueryParamSerializer
from todo.swagger import apidocs


@method_decorator(name='list', 
    decorator=swagger_auto_schema(**apidocs.TODO_LIST_VIEW))
@method_decorator(name='retrieve', 
    decorator=swagger_auto_schema(**apidocs.TODO_RETRIEVE_VIEW))
@method_decorator(name='destroy', 
    decorator=swagger_auto_schema(**apidocs.TODO_DESTROY_VIEW))
@method_decorator(name='partial_update', 
    decorator=swagger_auto_schema(**apidocs.TODO_PARTIAL_UPDATE_VIEW))
class TodoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsCreator]
    serializer_class = TodoSerializer

    def get_queryset(self):
        if self.action in ('list', 'random'):
            user = self.request.user
            completed = self.request.query_params.get('completed')
            serializer = TodoQueryParamSerializer(
                data={'completed': completed})

            if completed is not None and serializer.is_valid():
                return Todo.objects.filter(
                    creator_id=user.id, **serializer.validated_data)

            return Todo.objects.filter(creator_id=user.id)

        return Todo.objects.all()

    @swagger_auto_schema(**apidocs.TODO_CREATE_VIEW)
    def create(self, request):
        data = deepcopy(request.data)
        data.update({"creator_id": self.request.user.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, 
            status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(**apidocs.TODO_UPDATE_VIEW)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = deepcopy(request.data)
        data.update({"creator_id": self.request.user.id})
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

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
