from django.shortcuts import render
from .crowling import PortalCrowling, checkStaff
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def portalCrowling(request):
    context = '{ text :' + PortalCrowling() + '}'
    return Response(context, status=200)

@api_view(['GET'])
def staffUpdate(request):
    checkStaff()
    context = 'Test'
    return Response(context, status=200)
    
# Create your views here.
