from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from .models import Flower, Category


def home(request):
    flowers = Flower.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    if query:
        flowers = flowers.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'home.html', {
        'flowers': flowers,
        'categories': categories,
        'query': query or ''
    })


def flower_detail(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    return render(request, 'flower_detail.html', {'flower': flower})


@login_required
def flower_add(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST['title'].strip()
        category_id = request.POST['category']
        price = request.POST['price']
        stock = request.POST['stock']
        description = request.POST.get('description', '')

        flower = Flower(
            title=title,
            category_id=category_id,
            price=price,
            stock=stock,
            description=description
        )
        if 'image' in request.FILES:
            flower.image = request.FILES['image']
        flower.save()

        messages.success(request, f'"{title}" добавлен!')
        return redirect('flowers:home')

    return render(request, 'flower_form.html', {'categories': categories})


@login_required
def flower_delete(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    
    if request.method == 'POST':
        title = flower.title
        flower.delete()
        messages.success(request, f'Цветок "{title}" удалён!')
        return redirect('flowers:home')
    
    return render(request, 'flower_confirm_delete.html', {'flower': flower})


@login_required
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="catalog.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Каталог цветов", styles['Title']))
    story.append(Spacer(1, 20))

    data = [['№', 'Название', 'Категория', 'Цена', 'Остаток']]
    for i, flower in enumerate(Flower.objects.all(), 1):
        data.append([
            str(i),
            flower.title,
            flower.category.name,
            f"{flower.price} ₽",
            str(flower.stock)
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'), 
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))

    story.append(table)
    doc.build(story)
    return response

@login_required
def flower_delete(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    if request.method == 'POST':
        flower.delete()
        messages.success(request, 'Цветок удалён!')
        return redirect('flowers:home')
    return render(request, 'flower_confirm_delete.html', {'flower': flower})