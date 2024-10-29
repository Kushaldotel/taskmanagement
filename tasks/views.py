from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    #no need to mention is authentication permission here as it is already mentioned by default in settings.

    def get_queryset(self):
        # Return tasks for the logged-in user
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the logged-in user as the task owner
        serializer.save(user=self.request.user)
