from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from tasks.models import Project, Task, Comment
from datetime import date, timedelta

class ProjectTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_project(self):
        """Test creating a new project"""
        data = {
           "name": "Test Project",
           "description": "Test Description"
        }
        response = self.client.post('/api/projects/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().created_by, self.user) 

    def test_list_own_projects(self):
        """Test listing only projects created by the user"""
        Project.objects.create(name="User Project", created_by=self.user) 

        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "User Project")

class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.project = Project.objects.create(
            name="Test Project",
            created_by=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        """Test creating a new task"""
        data = {
            "title": "Test Task",
            "description": "Test Description",
            "status": "TODO",
            "project": self.project.id,
            "due_date": str(date.today() + timedelta(days=7))
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().created_by, self.user)

    def test_task_status_transition(self):
        """Test updating task status"""
        task = Task.objects.create(
            title="Test Task",
            status="TODO",
            project=self.project,
            created_by=self.user
        )
        data = {"status": "IN_PROGRESS"}
        response = self.client.patch(f'/api/tasks/{task.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=task.id).status, "IN_PROGRESS")

    def test_filter_tasks(self):
        """Test filtering tasks by status and project"""
        Task.objects.create(
            title="Todo Task",
            status="TODO",
            project=self.project,
            created_by=self.user
        )
        Task.objects.create(
            title="Done Task",
            status="DONE",
            project=self.project,
            created_by=self.user
        )

        response = self.client.get('/api/tasks/', {'status': 'TODO'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # تأكد من أن حالة الاستجابة صحيحة
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Todo Task")

class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.project = Project.objects.create(
            name="Test Project",
            created_by=self.user
        )
        self.task = Task.objects.create(
            title="Test Task",
            project=self.project,
            created_by=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_comment(self):
        """Test creating a new comment"""
        data = {
            "content": "Test Comment",
            "task": self.task.id
        }
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().user, self.user)

    def test_comment_visibility(self):
        """Test comment visibility for different users"""
        other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="pass123"
        )
        other_project = Project.objects.create(
            name="Other Project",
            created_by=other_user
        )
        other_task = Task.objects.create(
            title="Other Task",
            project=other_project,
            created_by=other_user
        )
        Comment.objects.create(
            content="Test Comment",
            task=self.task,
            user=self.user
        )
        Comment.objects.create(
            content="Other Comment",
            task=other_task,
            user=other_user
        )

        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # تأكد من أن حالة الاستجابة صحيحة
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], "Test Comment")
