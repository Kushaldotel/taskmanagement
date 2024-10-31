from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_completed']  # Allow filtering by completion status
    search_fields = ['title', 'description']  # Allow searching in title and description

    #no need to mention is authentication permission here as it is already mentioned by default in settings.

    def get_queryset(self):
        # Return tasks for the logged-in user
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the logged-in user as the task owner
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only reterive their own tasks
        return Task.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # Ensure that only the owner of the task can update it
        if self.get_object().user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this task.")
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure that only the owner of the task can delete it
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this task.")
        instance.delete()