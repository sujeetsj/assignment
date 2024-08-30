from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ImageProcessingRequest, Product
from .tasks import process_images_task
import uuid
import csv
from django.core.files.storage import default_storage

class UploadCSVView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.csv'):
            return Response({"error": "Only CSV files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the uploaded CSV file
        file_path = default_storage.save(f"csv/{file.name}", file)

        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Save initial request data to the database
        image_request = ImageProcessingRequest(request_id=request_id, status='Processing')
        image_request.save()

        # Asynchronous processing using Celery
        process_images_task.delay(request_id, file_path)

        return Response({"request_id": request_id}, status=status.HTTP_201_CREATED)

class StatusView(APIView):
    def get(self, request, request_id):
        image_request = get_object_or_404(ImageProcessingRequest, request_id=request_id)
        return Response({"request_id": request_id, "status": image_request.status})

class WebhookView(APIView):
    def post(self, request):
        # Handle webhook notification after image processing
        # This could be logging, sending an email, etc.
        return Response({"message": "Webhook received successfully"}, status=status.HTTP_200_OK)
