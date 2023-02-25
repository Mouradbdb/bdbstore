from django.shortcuts import render
from STORE.models import Product

def home(request):
    products = Product.objects.all().filter(is_avaliable = True)
    
    context = {
        'products':products
    }
    return render(request,'home.html',context)