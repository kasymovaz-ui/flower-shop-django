from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Flower, Category

def home(request):
    flowers = Flower.objects.filter(available=True)
    return render(request, 'home.html', {'flowers': flowers})

@login_required
def flower_add(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        category_id = request.POST['category']
        price = request.POST['price']
        stock = request.POST['stock']

        Flower.objects.create(
            title=title,
            slug=title.lower().replace(' ', '-').replace('ё', 'е'),
            category_id=category_id,
            price=price,
            stock=stock,
            available=True
        )
        messages.success(request, 'Цветок успешно добавлен!')
        return redirect('home')

    return render(request, 'flower_form.html', {'categories': categories})