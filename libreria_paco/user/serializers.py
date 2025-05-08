from user.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from payment.serializers import PaymentReadSerializer

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=3, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['name', 'lastName', 'email', 'password', 'roleId', 'paymentId']
        extra_kwargs = {
            'name': {'min_length': 2, 'max_length': 100},
            'lastName': {'min_length': 2, 'max_length': 150},
            'email': {
                'max_length': 320,
                'validators': [
                    UniqueValidator(queryset=User.objects.all(), message="Este email ya está registrado")
                ]
            },
            'password': {'write_only': True, 'min_length': 3},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserReadSerializer(serializers.ModelSerializer):
    paymentId = PaymentReadSerializer()
    roleId = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ['name', 'lastName', 'email', 'roleId', 'paymentId']
        read_only_fields = ['email', 'roleId']

class UserReadAllSerializer(serializers.ModelSerializer):
    roleId = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ['name', 'lastName', 'email', 'roleId']
        read_only_fields = ['email', 'roleId']

