# django and djangorestframework
from rest_framework import serializers
from django.conf import settings
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework import status

from .models import Admin, Squad

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class SquadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Squad
        fields = '__all__'