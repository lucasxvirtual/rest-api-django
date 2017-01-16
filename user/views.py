from django.shortcuts import render
from .serializers import UserSerializer, ThemeSerializer, CategorySerializer, UserCardSerializer
from .models import User, Theme, Card, Category, CardColor, UserCard
from .permissions import UserPermission
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes

# Create your views here.

class ApiUser(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (UserPermission,)

	def post(self, request):
		user = UserSerializer(data=request.data)
		if(user.is_valid()):
			user.save()
			return Response(user.data, status=201)
		return Response(user.errors, status=400)

	def get(self, request):
		user = UserSerializer(request.user)
		return Response(user.data)

class ApiTheme(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = ((IsAuthenticated,))

	def get(self, request):
		theme = Theme.objects.all()

		theme_serializer = ThemeSerializer(instance=theme, many=True)
	
		return Response(theme_serializer.data, status=200)

class ApiUserCard(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = ((IsAuthenticated,))

	def get(self, request):
		user = request.user
		user_card = UserCard.objects.all().filter(id_user = user.id)
		serializer = UserCardSerializer(user_card, many=True)

		return Response(serializer.data, status=200)

	def post(self, request):

		request.POST['id_user'] = request.user.id

		user_card = UserCardSerializer(data=request.data)

		if(user_card.is_valid()):
			user_card.save()
			return Response(user_card.data, status=201)
		return Response(user_card.errors, status=400)

	def put(self, request):
		user_card = get_object_or_404(UserCard, id_card=request.POST['id_card'], id_user=request.user.id)
		
		request.POST['id_user'] = request.user.id

		serializer = UserCardSerializer(user_card, data=request.data)

		if(serializer.is_valid()):
			serializer.save()
			return Response(serializer.data, status=200)

		return Response(serializer.errors, status=400)

	def delete(self, request):
		user_card = get_object_or_404(UserCard, id_card=request.POST['id_card'], id_user=request.user.id)
		worked = user_card.delete()
		return Response(status=410)