from django.urls import path
from .views import UploadCSVView, StatusView, WebhookView

urlpatterns = [
    path('upload/', UploadCSVView.as_view(), name='upload'),
    path('status/<str:request_id>/', StatusView.as_view(), name='status'),
    path('webhook/', WebhookView.as_view(), name='webhook'),
]
