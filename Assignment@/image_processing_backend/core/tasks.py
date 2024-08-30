from celery import shared_task
from PIL import Image
import requests
from io import BytesIO
import os
from django.conf import settings
from .models import ImageProcessingRequest, Product


@shared_task
def process_images_task(request_id, file_path):
    try:
        # Open and read the CSV file
        with open(os.path.join(settings.MEDIA_ROOT, file_path), mode='r') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                product_name = row['Product Name']
                input_urls = row['Input Image Urls'].split(',')
                output_urls = []

                for url in input_urls:
                    # Download the image
                    response = requests.get(url.strip())
                    img = Image.open(BytesIO(response.content))

                    # Compress the image by 50%
                    output_path = os.path.join(settings.MEDIA_ROOT, 'compressed', os.path.basename(url))
                    img.save(output_path, quality=50)

                    # Upload the compressed image (here it's stored locally; in production, use cloud storage)
                    output_url = f"/media/compressed/{os.path.basename(url)}"
                    output_urls.append(output_url)

                # Save product data to the database
                Product.objects.create(name=product_name, input_urls=','.join(input_urls),
                                       output_urls=','.join(output_urls))

        # Update request status to 'Completed'
        ImageProcessingRequest.objects.filter(request_id=request_id).update(status='Completed')
    except Exception as e:
        # Update request status to 'Failed'
        ImageProcessingRequest.objects.filter(request_id=request_id).update(status='Failed')
        raise e
