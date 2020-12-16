from .models import Comment
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment #Congressperson 모델을 기반으로 serialize
        fields = '__all__'