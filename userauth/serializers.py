from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields ='__all__'
        exclude = ['groups','user_permissions']

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['is_active']=True
        user_modules = User.objects.create(**validated_data)
        user_modules.set_password(validated_data.get('password'))
        user_modules.save()
        return user_modules

