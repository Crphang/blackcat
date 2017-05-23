from django.shortcuts import render
from admin.forms import ImageTabForm, EventTabForm, CategoryTabForm, EventCategoryTab
from django.utils import timezone

def index(request):
	return render(request, 'index.html')

def create_event(request):
    if request.method == 'POST':
        form = EventTabForm(request.POST, request.FILES)
        if form.is_valid():
        	form.save()
    else:
        form = EventTabForm()
        
    return render(request, 'upload.html', {
        'form': form
    })

def create_category(request):
    if request.method == 'POST':
        form = CategoryTabForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = CategoryTabForm()
        
    return render(request, 'upload.html', {
        'form': form
    })

def create_event_category(request):
    if request.method == 'POST':
        form = EventCategoryTab(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = EventCategoryTab()
        
    return render(request, 'upload.html', {
        'form': form
    })

def image_upload(request):
    if request.method == 'POST':
        form = ImageTabForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ImageTabForm()
        
    return render(request, 'upload.html', {
        'form': form
    })