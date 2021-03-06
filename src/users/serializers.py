from rest_framework import serializers
from .models import Psicologo
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+\- ]+$'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'user': self.user.username})
        # and everything else you want to send in the response
        return data


class UserSerializer(serializers.Serializer):    
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all()), MyValidator()], 
        # unique=True,
        label="Username Address",

    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        # unique=True,
        label="Email Address",
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class PsicologoSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Psicologo
        fields = ('user', 'nCRP', 'bio', 'genero', 'name')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        psicologo = Psicologo.objects.create(user=user, **validated_data)
        return psicologo

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            user = validated_data.pop('user')
            if 'username' in user:
                instance.user.username = user.get('username', instance.user.username)
            if 'email' in user:
                instance.user.email = user.get('email', instance.user.email)
        if 'nCRP' in validated_data:
            instance.nCRP = validated_data.get('nCRP', instance.nCRP)   
        if 'bio' in validated_data:
            instance.bio = validated_data.get('bio', instance.bio)   
        if 'genero' in validated_data:
            instance.genero = validated_data.get('genero', instance.genero)   
        if 'name' in validated_data:
            instance.name = validated_data.get('name', instance.name)          
            
        instance.user.save()

        return super().update(instance, validated_data)

    def validate_nCRP(self, nCRP):
        if len(nCRP) != 11:
            raise serializers.ValidationError('numero de caracteres invalido')

        return nCRP
