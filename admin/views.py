from gc import get_objects
from django.shortcuts import render
from home.models import Homestay

# Create your views here.
def admin_view(request):
    homestays = Homestay.objects.all()
    context = {
        'homestays': homestays
    }
    render(request, 'homestay.html',context)