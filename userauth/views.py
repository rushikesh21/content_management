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

class Register(APIView):
	permission_classes = (AllowAny, )
	def post(self, request, format=None):
		data = request.data
		pattern = '[A-Z]+[a-z]'
		if len(data.get('password'))>7 and re.search(pattern, data.get('password')):
			serializer=UserSerializer(data=data)
			if serializer.is_valid():
				serializer.save()

				return Response(serializer.data,status=status.HTTP_200_OK)
			else:
				return Response({'error-msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

		else:
			return Response({'error-msg':'Check password rules - Min 8 length, 1 uppercase, 1 lowercase'},status=status.HTTP_400_BAD_REQUEST)

class User_login(APIView):
	permission_classes = (AllowAny, )
	def post(self, request, format=None):
		data = request.data
		email = data.get('email').lower()
		password = data.get('password')
		user = User.objects.filter(email__iexact=email)
		if user.exists():
			user = user.last()
			if user.check_password(password):
				request.session['email'] = user.email
				request.session['id'] = user.id
				login(request, user)
				authenticate(email=email, password=password)
				serializer = UserSerializer(user, many=False)
				token, created = Token.objects.get_or_create(user=user)
				token_data = {"token": token.key,"user":serializer.data}
				return Response(token_data,status=status.HTTP_200_OK)
			else:
				return Response({'msg':'Incorrect username/password'}, status=status.HTTP_400_BAD_REQUEST)
		else :
			return Response({'msg':'User does not exist in the system'}, status=status.HTTP_400_BAD_REQUEST)