from .models import Congressperson, Saying
import json
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from pathlib import Path
from django.shortcuts import get_object_or_404
 

def search(request, district):
    info_dict = model_to_dict(Congressperson.objects.get(district=district))
    saying_dict = model_to_dict(Saying.objects.order_by("?").first())
    if info_dict or saying_dict:
        to_json = {**info_dict, **saying_dict}
        return JsonResponse(to_json)
