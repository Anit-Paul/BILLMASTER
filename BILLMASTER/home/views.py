from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'home/index.html')
def home_product(request):
    return render(request,'home/index2.html')