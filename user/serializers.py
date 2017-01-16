from .models import User, Theme, Category, Card, CardColor, UserCard
from rest_framework import serializers
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'name', 'password', 'email')
		write_only_fields = ('password',)
		read_only_fields = ('id',)

	def create(self, validated_data):
		user = User.objects.create(
			name=validated_data['name'],
			email=validated_data['email'],
		)

		user.set_password(validated_data['password'])
		user.save()

		return user

	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.updated_at = datetime.now()

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id', 'name', 'id_theme', 'order', 'country', 'updated_at', 'created_at')

class CardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Card
		fields = ('id', 'name', 'mode', 'card_picture', 'image', 'audio', 'text', 'downloads', 'price', 'tags', 'character', 'country', 'id_category', 'id_theme', 'updated_at', 'created_at')


class ThemeSerializer(serializers.ModelSerializer):

	categories = CategorySerializer(many=True)
	cards = CardSerializer(many=True)

	class Meta:
		model = Theme
		fields = ('id', 'name', 'description', 'image', 'order', 'updated_at', 'created_at', 'categories', 'cards')

class UserCardSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserCard
		fields = ('id_user', 'id_card', 'updated_at', 'created_at')

	def create(self, validated_data):
		return UserCard.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.updated_at = datetime.now()
		instance.save()
		return instance




