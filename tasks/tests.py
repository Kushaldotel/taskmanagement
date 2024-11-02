from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task
import json

class TaskListCreateViewTests(APITestCase):
    def setUp(self):
        # Create a user and obtain JWT tokens
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Set URLs
        self.task_list_create_url = reverse('task-list-create')

    def test_list_tasks_for_authenticated_user(self):
        """
        Ensure only the authenticated user's tasks are listed.
        """
        # Create a task for the user
        Task.objects.create(user=self.user, title="User Task 1", description="Description 1")
        # Create a task for another user
        other_user = User.objects.create_user(username="otheruser", password="otherpassword")
        Task.objects.create(user=other_user, title="Other User Task", description="Other Description")

        # Make a GET request to retrieve tasks
        response = self.client.get(self.task_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only list the task for the authenticated user
        self.assertEqual(response.data[0]["title"], "User Task 1")

    def test_create_task_for_authenticated_user(self):
        """
        Ensure the authenticated user can create a task.
        """
        data = {
            "title": "New Task",
            "description": "New Task Description",
            "is_completed": False
        }
        response = self.client.post(self.task_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.user, self.user)  # Check that the task is assigned to the logged-in user
        self.assertEqual(task.title, "New Task")

    def test_unauthenticated_access(self):
        """
        Ensure that unauthenticated users cannot access the task list.
        """
        # Remove credentials to simulate unauthenticated request
        self.client.credentials()
        response = self.client.get(self.task_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TaskDetailViewTests(APITestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

        # Authenticate user1
        self.client.force_authenticate(user=self.user1)

        # Create a task for user1 and user2
        self.task_user1 = Task.objects.create(user=self.user1, title="User1 Task", description="Task for user1")
        self.task_user2 = Task.objects.create(user=self.user2, title="User2 Task", description="Task for user2")

    def test_retrieve_task(self):
        # Retrieve task for user1
        url = reverse('task-detail', args=[self.task_user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task_user1.title)

    def test_update_task(self):
        # Update task for user1
        url = reverse('task-detail', args=[self.task_user1.id])
        data = json.dumps({'title': 'Updated Task Title'})  # Use json.dumps to ensure proper formatting
        response = self.client.patch(url, data, content_type='application/json')

        # # Log the response data for debugging
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task_user1.refresh_from_db()
        self.assertEqual(self.task_user1.title, 'Updated Task Title')


    def test_delete_task(self):
        # Delete task for user1
        url = reverse('task-detail', args=[self.task_user1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task_user1.id).exists())

    def test_access_control_for_other_user(self):
        # Try to retrieve user2's task with user1's authentication
        url = reverse('task-detail', args=[self.task_user2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to update user2's task with user1's authentication
        data = {'title': 'Unauthorized Update Attempt'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to delete user2's task with user1's authentication
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)