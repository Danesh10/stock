from django.http import JsonResponse
import requests
# Create your views here.
def req(request):
    response = requests.get("http://localhost:8000/base/stock/?name=abc&short_name=dk")
    data = response.json()
    return JsonResponse(dict(validation="request sent", status=True))