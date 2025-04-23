from payment.models import Payment
from rest_framework import serializers

class PaymentCreateSerializer(serializers.ModelSerializer):
    cvc_exists = serializers.SerializerMethodField()
    class Meta:
        model = Payment
        fields = ['number', 'name', 'cvc', 'cvc_exists', 'expiration']
        extra_kwargs = {
            'name':{'min_length':4, 'max_length':300},
            'cvc':{'write_only': True, 'min_length': 3, 'max_length':4},
            'number':{'min_length':12, 'max_length':19}
        }
        #con el write_only=True, consigo que, al llamar al serializer, el cvc no sea visible

    def get_cvc_exists(self, obj):
        return bool(obj.cvc)
    
class PaymentReadSerializer(serializers.ModelSerializer):
    number_card  = serializers.SerializerMethodField()
    cvc_exists = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['name', 'number_card', 'cvc_exists', 'expiration']

    #self es el metodo serializer, mientras que obj representa models.py de payment
    def get_number_card(self, obj):
        numero_tarjeta = str(obj.number)
        return '...'+numero_tarjeta[-4:]
    
    def get_cvc_exists(self, obj):
        return bool(obj.cvc)
