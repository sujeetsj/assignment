from django.db import models

class ImageProcessingRequest(models.Model):
    request_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    input_urls = models.TextField()
    output_urls = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
