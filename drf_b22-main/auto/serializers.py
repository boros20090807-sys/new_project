from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Games,GamesReview,SystemRequirements,Publisher
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validate_data):
        user = User.objects.create_user(
            username = validate_data['username'],
            email = validate_data['email'],
            password = validate_data['password']
        )
        Token.objects.create(user=user)
        return user

class loginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if user is None:
            raise serializers.ValidationError(
                'Invalid username or pasword'
            )

        data['user'] = user

        return data

class GamesSerializer(serializers.ModelSerializer):
    publisher = serializers.SlugRelatedField(
                slug_field='title',
                queryset=Publisher.objects.all()
    )

    class Meta:
        model = Games
        fields = '__all__'

class GamesReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamesReview
        fields = '__all__'

        
class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemRequirements
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

