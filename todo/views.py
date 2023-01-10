from copy import deepcopy

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class TodoViewSet(ModelViewSet):

    serializer_class = TodoSerializer

    def get_queryset(self):
        """
        Return a list of all the Todo objects
        for the currently authenticated user.
        """
        user = self.request.user
        return Todo.objects.filter(creator_id=user.id)

    def create(self, request):
        data = deepcopy(request.data)
        data.update({"creator_id": self.request.user.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def random(self, request, pk=None):
        pass
