from django.urls import path

from .views import get_data, process_file
from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(["GET"])
def hello(req):
    return Response({"message", "hello world"})

urlpatterns = [
    path("process-file", process_file, name="Process File"),
    path("get-data", get_data, name="Get Data"),
    path("", hello, name="hello")
]
