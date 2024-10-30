"""
This module defines the models for the Task application.

Classes:
    Project: Represents a project, with fields for name, description, creation date, and creator.
    Task: Represents a task, with fields for title, description, status, due date, assigned user, project, creation date, and creator.
    Comment: Represents a comment on a task, with fields for content, creation date, task, and user.
"""

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
    """
    Represents a project.

    Fields:
        name (CharField): The name of the project.
        description (TextField): The description of the project.
        created_at (DateTimeField): The creation date of the project.
        created_by (ForeignKey): The user who created the project.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the project.

        Returns:
            str: The name of the project.
        """
        return self.name

class Task(models.Model):
    """
    Represents a task.

    Fields:
        title (CharField): The title of the task.
        description (TextField): The description of the task.
        status (CharField): The status of the task (TODO, IN_PROGRESS, DONE).
        due_date (DateField): The due date of the task.
        assigned_to (ForeignKey): The user assigned to the task.
        project (ForeignKey): The project the task belongs to.
        created_at (DateTimeField): The creation date of the task.
        created_by (ForeignKey): The user who created the task.
    """
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    due_date = models.DateField(default=None)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

    def __str__(self):
        """
        Returns a string representation of the task.

        Returns:
            str: The title of the task.
        """
        return self.title

class Comment(models.Model):
    """
    Represents a comment on a task.

    Fields:
        content (TextField): The content of the comment.
        created_at (DateTimeField): The creation date of the comment.
        task (ForeignKey): The task the comment belongs to.
        user (ForeignKey): The user who created the comment.
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the comment.

        Returns:
            str: The content of the comment and the user who created it.
        """
        return f'Comment by {self.user.username} on {self.task.title}'
