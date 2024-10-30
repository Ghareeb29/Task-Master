from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Project, Task, Comment, models

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']

    @extend_schema(
        summary="List projects",
        description="Get a list of all projects created by the authenticated user.",
        responses={200: ProjectSerializer(many=True)},
        tags=['projects']
    )
    def list(self, request):
        return super().list(request)

    @extend_schema(
        summary="Create project",
        description="Create a new project for the authenticated user.",
        request=ProjectSerializer,
        responses={201: ProjectSerializer},
        tags=['projects']
    )
    def create(self, request):
        return super().create(request)

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'project', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'status']

    @extend_schema(
        summary="List tasks",
        description="Get a list of all tasks accessible to the authenticated user.",
        parameters=[
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.STR,
                description='Filter tasks by status (TODO, IN_PROGRESS, DONE)',
                required=False
            ),
            OpenApiParameter(
                name='project',
                type=OpenApiTypes.INT,
                description='Filter tasks by project ID',
                required=False
            ),
        ],
        responses={200: TaskSerializer(many=True)},
        tags=['tasks']
    )
    def list(self, request):
        return super().list(request)

    @extend_schema(
        summary="Create task",
        description="Create a new task within a project.",
        request=TaskSerializer,
        responses={
            201: TaskSerializer,
            400: {"type": "object", "properties": {
                "error": {"type": "string"}
            }}
        },
        tags=['tasks']
    )
    def create(self, request):
        return super().create(request)

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            models.Q(created_by=user) |
            models.Q(assigned_to=user) |
            models.Q(project__created_by=user)
        ).distinct()
