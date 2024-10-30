"""
This module provides views for the tasks application.

It includes viewsets for projects, tasks, and comments, which handle CRUD operations
and provide API endpoints for the frontend to interact with.

Classes:
    ProjectViewSet: Handles CRUD operations for projects.
    TaskViewSet: Handles CRUD operations for tasks.
    CommentViewSet: Handles CRUD operations for comments.

Functions:
    None

Variables:
    None

Exceptions:
    None
"""

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer

@extend_schema_view(
    list=extend_schema(description='List all projects', responses={200: ProjectSerializer(many=True)}),
    create=extend_schema(description='Create a new project', request=ProjectSerializer, responses={201: ProjectSerializer}),
    retrieve=extend_schema(description='Retrieve a project by ID', responses={200: ProjectSerializer}),
    update=extend_schema(description='Update a project by ID', request=ProjectSerializer, responses={200: ProjectSerializer}),
    partial_update=extend_schema(description='Partial update a project by ID', request=ProjectSerializer, responses={200: ProjectSerializer}),
    destroy=extend_schema(description='Delete a project by ID', responses={204: None})
)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

@extend_schema_view(
    list=extend_schema(description='List all tasks', responses={200: TaskSerializer(many=True)}),
    create=extend_schema(description='Create a new task', request=TaskSerializer, responses={201: TaskSerializer}),
    retrieve=extend_schema(description='Retrieve a task by ID', responses={200: TaskSerializer}),
    update=extend_schema(description='Update a task by ID', request=TaskSerializer, responses={200: TaskSerializer}),
    partial_update=extend_schema(description='Partial update a task by ID', request=TaskSerializer, responses={200: TaskSerializer}),
    destroy=extend_schema(description='Delete a task by ID', responses={204: None})
)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

@extend_schema_view(
    list=extend_schema(description='List all comments', responses={200: CommentSerializer(many=True)}),
    create=extend_schema(description='Create a new comment', request=CommentSerializer, responses={201: CommentSerializer}),
    retrieve=extend_schema(description='Retrieve a comment by ID', responses={200: CommentSerializer}),
    update=extend_schema(description='Update a comment by ID', request=CommentSerializer, responses={200: CommentSerializer}),
    partial_update=extend_schema(description='Partial update a comment by ID', request=CommentSerializer, responses={200: CommentSerializer}),
    destroy=extend_schema(description='Delete a comment by ID', responses={204: None})
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
