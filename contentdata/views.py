from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *
from rest_framework.generics import (
	UpdateAPIView,
	ListAPIView,
	ListCreateAPIView)
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
import re


class ContentView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, format=None):
			user=request.user
			data = request.data
			data['user']=user.id
			serializer=ContentSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data,status=status.HTTP_200_OK)
			else:
				return Response({'error_message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, format=None):
			user=request.user
			if user.role=="admin":
				contentqueryset=Content.objects.filter()
			else:
				contentqueryset=Content.objects.filter(user_id=user.id)
			serializer=ContentSerializer(contentqueryset,many=True)
			return Response(serializer.data,status=status.HTTP_200_OK)


class ContentEditView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request,pk, format=None):
			user=request.user
			data = request.data
			data['user']=user.id
			if user.role=='admin':
				contentqueryset=Content.objects.get(id=pk)
				serializer=ContentSerializer(contentqueryset,data=data)
				if serializer.is_valid():
					serializer.save()

					return Response(serializer.data,status=status.HTTP_200_OK)
				else:
					return Response({'error_message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
			else:
				contentqueryset=Content.objects.filter(user_id=user.id,id=pk)
				if contentqueryset.exists():
					serializer=ContentSerializer(contentqueryset.last(),data=data)
					if serializer.is_valid():
						serializer.save()
						return Response(serializer.data,status=status.HTTP_200_OK)
					else:
						return Response({'error_message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
				else:
					return Response({'error_message':'Content Not found'}, status=status.HTTP_400_BAD_REQUEST)


class ContentDetailView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request,pk, format=None):
			user=request.user
			if user.role=='admin':
				contentqueryset=Content.objects.filter(id=pk)
				if contentqueryset.exists():
					serializer=ContentSerializer(contentqueryset.last(),many=False)
					return Response(serializer.data,status=status.HTTP_200_OK)
				else:
					return Response({'error_message':'Content Not Found'}, status=status.HTTP_400_BAD_REQUEST)
			else:
				contentqueryset=Content.objects.filter(user_id=user.id,id=pk)
				if contentqueryset.exists():
					serializer=ContentSerializer(contentqueryset.last(),many=False)
					return Response(serializer.data,status=status.HTTP_200_OK)
				else:
					return Response({'error_message':'Content Not found'}, status=status.HTTP_400_BAD_REQUEST)


class ContentDeleteView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request,pk, format=None):
			user=request.user

			if user.role=='admin':
				contentqueryset=Content.objects.filter(id=pk)
				if contentqueryset.exists():
					contentqueryset.delete()
					return Response({'message':'Success'},status=status.HTTP_200_OK)
				else:
					return Response({'error_message':'Content Not Found'}, status=status.HTTP_400_BAD_REQUEST)
			else:
				contentqueryset=Content.objects.filter(user_id=user.id,id=pk)
				if contentqueryset.exists():
					contentqueryset.delete()
					return Response({'message':'Success'},status=status.HTTP_200_OK)
				else:
					return Response({'error_message':'Content Not found'}, status=status.HTTP_400_BAD_REQUEST)