from django.contrib import admin
from .models import ImageProcessingRequest, Product

@admin.register(ImageProcessingRequest)
class ImageProcessingRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'status', 'created_at')
    search_fields = ('request_id', 'status')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
