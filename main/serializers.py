from rest_framework import serializers
from .models import *

class BlackSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Black
        fields = ['id', 'name', 'nickname', 'img', 'color', 'frame']  
    
    def get_nickname(self,obj):
        return obj.user.nickname

class WhiteSerializer(serializers.ModelSerializer):
    class Meta:
        model=White
        fields=['id', 'name', 'nickname', 'img', 'color', 'frame'] 
        
    def get_nickname(self,obj):
        return obj.user.nickname