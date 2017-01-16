from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import datetime

def directory_path(instance, filename):
	ret = ''
	if(isinstance(instance, User)):
		ret = 'users/{0}/{1}'.format(instance.email, filename)
	elif(isinstance(instance, Theme)):
		ret = 'themes/{0}/{1}'.format(instance.name + str(instance.created_at.day) + str(instance.created_at.month) + str(instance.created_at.year) + str(instance.created_at.hour) + str(instance.created_at.minute) + str(instance.created_at.second), filename)
	elif(isinstance(instance, Card)):
		ret = 'cards/{0}/thumbnail/{1}'.format(instance.name + str(instance.created_at.day) + str(instance.created_at.month) + str(instance.created_at.year) + str(instance.created_at.hour) + str(instance.created_at.minute) + str(instance.created_at.second), filename)
		
	return ret

def card_image_directory_path(instance, filename):
	return 'cards/{0}/image/{1}'.format(instance.name + str(instance.created_at.day) + str(instance.created_at.month) + str(instance.created_at.year) + str(instance.created_at.hour) + str(instance.created_at.minute) + str(instance.created_at.second), filename)

def card_audio_directory_path(instance, filename):
	return 'cards/{0}/audio/{1}'.format(instance.name + str(instance.created_at.day) + str(instance.created_at.month) + str(instance.created_at.year) + str(instance.created_at.hour) + str(instance.created_at.minute) + str(instance.created_at.second), filename)

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if(not email):
			raise ValueError('Users must have an email')

		user = self.model(
			email=self.normalize_email(email),
		)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, password):
		"""
		Creates and saves a superuser with the given email and password.
		"""
		user = self.create_user(email,
			password=password,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	email = models.CharField(max_length=100, unique=True)
	name = models.CharField(max_length=100)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'

	def get_full_name(self):
		# The user is identified by their email address
		return self.email

	def get_short_name(self):
		# The user is identified by their email address
		return self.email

	def __str__(self):              # __unicode__ on Python 2
		return self.email

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)


class Theme(models.Model):
	name = models.CharField(max_length = 100, null = False)
	description = models.CharField(max_length = 100, null = True, blank = True)
	image = models.FileField(upload_to = directory_path)
	order = models.IntegerField(null = True, blank = True)
	updated_at = models.DateTimeField(default = datetime.now, null = False, blank = False)
	created_at = models.DateTimeField(default = datetime.now, null = False, blank = False)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length = 100, null = False)
	id_theme = models.ForeignKey(Theme, on_delete = models.CASCADE, db_column = 'id_theme', related_name='categories')
	order = models.IntegerField(null = True, blank = True)
	country = models.CharField(max_length = 50, null = True, blank = True)
	updated_at = models.DateTimeField(default = datetime.now, null = False, blank = False)
	created_at = models.DateTimeField(default = datetime.now, null = False, blank = False)

	def __str__(self):
		return self.name

class Card(models.Model):
	name = models.CharField(max_length = 100, null = False)
	mode = models.CharField(max_length = 100, null = False, blank = False)
	card_picture = models.FileField(upload_to = directory_path)
	image = models.FileField(upload_to = card_image_directory_path, null = True, blank = True)
	audio = models.FileField(upload_to = card_audio_directory_path, null = True, blank = True)
	text = models.CharField(max_length = 100, null = True, blank = True)
	downloads = models.IntegerField(default = 0)
	price = models.CharField(max_length = 10, null = True, blank = True, default = 'free')
	tags = models.CharField(max_length = 300, null = True, blank = True)
	character = models.CharField(max_length = 100, null = True, blank = True)
	country = models.CharField(max_length = 50, null = True, blank = True)
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, db_column = 'creator')
	id_category = models.ForeignKey(Category, on_delete = models.CASCADE, db_column = 'id_category', null = True, blank = True, related_name='cards')
	id_theme = models.ForeignKey(Theme, on_delete = models.CASCADE, db_column = 'id_theme', related_name='cards')
	updated_at = models.DateTimeField(default = datetime.now, null = False, blank = False)
	created_at = models.DateTimeField(default = datetime.now, null = False, blank = False)

	def __str__(self):
		return self.name

class UserCard(models.Model):
	id_user = models.ForeignKey(User, on_delete = models.CASCADE, db_column = 'id_user')
	id_card = models.ForeignKey(Card, on_delete = models.CASCADE, db_column = 'id_card')
	updated_at = models.DateTimeField(default = datetime.now, null = False, blank = False)
	created_at = models.DateTimeField(default = datetime.now, null = False, blank = False)

	def __str__(self):
		return str(self.id_usuario) + " " + str(self.id_card)

	class Meta:
		unique_together = ('id_user', 'id_card')

class CardColor(models.Model):
	id_card = models.ForeignKey(Card, on_delete = models.CASCADE, db_column = 'id_card')
	length = models.IntegerField(null = True, blank = True)
	order = models.IntegerField(null = True, blank = True)
	color = models.CharField(max_length = 10, null = True, blank = True)
	updated_at = models.DateTimeField(default = datetime.now, null = False, blank = False)
	created_at = models.DateTimeField(default = datetime.now, null = False, blank = False)

	def __str__(self):
		return  str(self.id_card) + " " + self.color