from user.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from payment.serializers import PaymentReadSerializer

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'lastName', 'email', 'password', 'roleId', 'paymentId']
        extra_kwargs = {
            'name':{'min_length':2, 'max_length':100},
            'lastName':{'min_length':2, 'max_length':150},
            'email':{'max_length':320,
                     'validators':[UniqueValidator(queryset=User.objects.all(), message="Este email ya está registrado")]},
            'password':{'write_only': True,
                        'min_length': 1, 
                        'style':{'input_type':'password'}},
        }
        #con el write_only=True, consigo que, al llamar al serializer, la password no sea visible

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

