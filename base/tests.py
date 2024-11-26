from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class TaskManagerTestCase(TestCase):

    def setUp(self):
        """Set up test users and sample tasks."""
        self.client = Client()
        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password456')
        
        # Create tasks for user1
        self.task1 = Task.objects.create(user=self.user1, title="Task 1", description="Test task 1", complete=False, complex=False)
        self.task2 = Task.objects.create(user=self.user1, title="Task 2", description="Test task 2", complete=True, complex=True)

        # Task list URL
        self.task_list_url = reverse('task-list')
        self.task_create_url = reverse('task-create')
        self.task_detail_url = reverse('task-detail', args=[self.task1.id])
        self.task_update_url = reverse('task-update', args=[self.task1.id])
        self.task_delete_url = reverse('task-delete', args=[self.task1.id])
        self.login_url = reverse('login')
        self.register_url = reverse('register')

    def test_login_required_redirect(self):
        """Ensure unauthenticated users are redirected to the login page."""
        response = self.client.get(self.task_list_url)
        self.assertRedirects(response, f"{self.login_url}?next={self.task_list_url}")

    def test_authenticated_user_access_task_list(self):
        """Test task list view for an authenticated user."""
        self.client.login(username='testuser1', password='password123')
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")

    def test_task_creation(self):
        """Test task creation for logged-in user."""
        self.client.login(username='testuser1', password='password123')
        response = self.client.post(self.task_create_url, {
            'title': 'New Task',
            'description': 'Description of new task',
            'complete': False,
            'complex': False
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_update(self):
        """Test updating an existing task."""
        self.client.login(username='testuser1', password='password123')
        response = self.client.post(self.task_update_url, {
            'title': 'Updated Task',
            'description': 'Updated description',
            'complete': True,
            'complex': True
        })
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task')
        self.assertTrue(self.task1.complete)

    def test_task_delete(self):
        """Test task deletion."""
        self.client.login(username='testuser1', password='password123')
        response = self.client.post(self.task_delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_task_list_search(self):
        """Test searching for tasks."""
        self.client.login(username='testuser1', password='password123')
        response = self.client.get(self.task_list_url, {'search-area': 'Task 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')

    def test_register_new_user(self):
        """Test user registration."""
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to task list
        self.assertTrue(User.objects.filter(username='newuser').exists())
