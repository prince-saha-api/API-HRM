from django.shortcuts import render
# from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from department import models as MODELS_D
from department.serializer import serializers as SRLZER_D
from rest_framework.response import Response
from rest_framework import status
from helps.common.generic import Generichelps as ghelp

# Create your views here.
