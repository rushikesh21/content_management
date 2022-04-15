from rest_framework import serializers
from .models import *

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields ='__all__'

    def create(self, validated_data):
        Categories_data=validated_data.pop('Categories')
        user_modules = Content.objects.create(**validated_data)
        user_modules.save()
        for i in Categories_data:
            user_modules.Categories.add(i)
        return user_modules

    def update(self, instance, validated_data):
        Categories_data = validated_data.pop('Categories')
        instance = super(ContentSerializer, self).update(instance, validated_data)
        for i in Categories_data:
            instance.Categories.add(i)
        return instance


