from django.urls import path

from .views import get_data, process_file

urlpatterns = [
    path("process-file", process_file, name="Process File"),
    path("get-data", get_data, name="Get Data"),
]
