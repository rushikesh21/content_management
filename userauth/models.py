from django.db import models

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email,password, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		# if not email:
		#     raise ValueError('The given email must be set')
		# # email = self.normalize_email(email)
		user = self.model(email=email,**extra_fields)
		user.set_password(password)
		user.is_staff = True
		user.is_superuser =True
		user.role = 'admin'
		user.save(using=self._db)
		return user

	def create_user(self,email, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self,email, password, **extra_fields):
		extra_fields.setdefault('is_superuser', True)
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
	user_type = (
	("admin", "ADMIN"),
	("normal", "NORMAL"))
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=100)
	full_name = models.CharField(max_length=300)
	phone = models.IntegerField(null=True,blank=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	role = models.CharField( max_length = 20, choices = user_type, default = 'normal')
	address=models.CharField(max_length=500,null=True,blank=True)
	city=models.CharField(max_length=500,null=True,blank=True)
	state=models.CharField(max_length=300,null=True,blank=True)
	country=models.CharField(max_length=500,null=True,blank=True)
	pincode = models.IntegerField(null=True,blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	objects = UserManager()
	USERNAME_FIELD = "email"

	def __str__(self):
		return "%s" % self.full_name
