from django.urls import path
from .views import process_file

urlpatterns = [path("process-file", process_file, name="Process File")]
