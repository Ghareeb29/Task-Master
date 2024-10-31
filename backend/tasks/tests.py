from django.test import Client, TestCase
from django.contrib.auth.models import User
from .models import Project, Task, Comment

class ProjectViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_project(self):
        data = {'name': 'Test Project', 'description': 'This is a test project.'}
        response = self.client.post('/api/projects/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), 1)

    def test_list_projects(self):
        Project.objects.create(name='Test Project', description='This is a test project.', created_by=self.user)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

class TaskViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.project = Project.objects.create(name='Test Project', description='This is a test project.', created_by=self.user)
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_task(self):
        data = {
            'title': 'Test Task',
            'description': 'This is a test task.',
            'project': self.project.id
        }
        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)

    def test_list_tasks(self):
        Task.objects.create(title='Test Task', description='This is a test task.', project=self.project, created_by=self.user)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

class CommentViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.project = Project.objects.create(name='Test Project', description='This is a test project.', created_by=self.user)
        self.task = Task.objects.create(title='Test Task', description='This is a test task.', project=self.project, created_by=self.user)
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_comment(self):
        data = {
            'content': 'This is a test comment.',
            'task': self.task.id
        }
        response = self.client.post('/api/comments/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)

    def test_list_comments(self):
        Comment.objects.create(content='This is a test comment.', task=self.task, user=self.user)
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
