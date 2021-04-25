from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

import logging
logger = logging.getLogger("error")



@csrf_exempt
@require_http_methods(["GET"])
def health(request):

    return JsonResponse({"status":"UP"})