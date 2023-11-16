from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Feedback
        fields = ['id', 'category', 'title', 'text', 'created_at', 'user']

    def get_user(self, obj):
        return obj.user.username if obj.user else None