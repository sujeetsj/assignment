from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import ImageProcessingRequest, Product
import tempfile
import os


class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.upload_url = reverse('upload')
        self.status_url = lambda request_id: reverse('status', args=[request_id])
        self.webhook_url = reverse('webhook')

    def test_upload_api(self):
        # Create a temporary CSV file for testing
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        temp_file.write(b"Serial Number,Product Name,Input Image Urls\n1,Product1,https://example.com/image1.jpg")
        temp_file.close()

        # Open the file in binary mode
        with open(temp_file.name, 'rb') as csv_file:
            response = self.client.post(self.upload_url, {'file': csv_file}, format='multipart')

        # Assert the response status code and structure
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('request_id', response.data)

        # Clean up the temporary file
        os.unlink(temp_file.name)

    def test_status_api(self):
        # Create a sample request object
        image_request = ImageProcessingRequest.objects.create(request_id='1234', status='Processing')

        # Make a GET request to the status API
        response = self.client.get(self.status_url('1234'))

        # Assert the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Processing')

    def test_webhook_api(self):
        # Make a POST request to the webhook API
        response = self.client.post(self.webhook_url, data={'message': 'test'})

        # Assert the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Webhook received successfully')
