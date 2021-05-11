from rest_framework import viewsets
from .models import Lead
from .serializers import LeadSerializer
from django.contrib.auth.models import User


class LeadViewSet(viewsets.ModelViewSet):
    serializer_class = LeadSerializer
    queryset = Lead.objects.all().select_related('assigned_to')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        obj = self.get_object()

        lead_id = self.request.data['assigned_to']

        if lead_id:
            user = User.objects.get(pk=lead_id)
            serializer.save(assigned_to=user)
        else:
            serializer.save()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)