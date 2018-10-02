from django.shortcuts import render
from .models import Product, Designer


def index(request):
    qs = Product.objects.all()
    designers = Designer.objects.all()
    if request.method == 'POST':
        selection = request.POST['list_designers']
        if selection != '0':
            qs = qs.filter(designer=selection)
    return render(request, 'plm/index.html', {'qs': qs, 'designers': designers})
