from rest_framework import serializers
from .models import ImageProcessingRequest, Product

class ImageProcessingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProcessingRequest
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
