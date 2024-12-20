from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .pagination import DefaultPagination
from .serializers import TaskSerializer, TaskCreateSerializer


class TaskViewSet(ModelViewSet):

    queryset = Task.objects.all()
    search_fields = ['name', 'description']
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TaskCreateSerializer
        return TaskSerializer
