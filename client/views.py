from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from .models import Client, Note    
from .serializers import ClientSerializer, NoteSerializer


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        obj = self.get_object()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self):
        client_id = self.request.GET.get('client_id')
        return self.queryset.filter(client_id=client_id)

    def perform_create(self, serializer):
        client_id = self.request.data['client_id']
        serializer.save(created_by=self.request.user, client_id=client_id)
