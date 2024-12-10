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

class BlackPostDetailSerializer(serializers.ModelSerializer):
    nickname=serializers.SerializerMethodField()
    is_owner=serializers.SerializerMethodField()

    class Meta:
        model=Black
        fields = ['nickname', 'category', 'name', 'information', 'description', 'is_owner', 'img', 'color', 'frame']
        
        def get_nickname(self, obj):
            return obj.user.nickname
    
        def get_is_owner(self,obj):
            request=self.context.get('request')
            if request and request.user==obj.user:
                return True
            return False

class WhitePostDetailSerializer(serializers.ModelSerializer):
    nickname=serializers.SerializerMethodField()
    is_owner=serializers.SerializerMethodField()

    class Meta:
        model=White
        fields = ['nickname', 'category', 'name', 'information', 'description', 'is_owner', 'img', 'color', 'frame']
        
        def get_nickname(self, obj):
            return obj.user.nickname
    
        def get_is_owner(self,obj):
            request=self.context.get('request')
            if request and request.user==obj.user:
                return True
            return False