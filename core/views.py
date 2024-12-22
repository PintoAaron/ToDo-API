from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .pagination import DefaultPagination
from .serializers import TaskSerializer, TaskCreateSerializer
from .filters import TaskFilter


class TaskViewSet(ModelViewSet):

    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description']
    filterset_class = TaskFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TaskCreateSerializer
        return TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
