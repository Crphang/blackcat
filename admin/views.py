from django.shortcuts import render
from api.models import UserTab, EventTab, ImageTab
from admin.forms import ImageTabForm, ImageForm, EventTabForm, CategoryTabForm, EventCategoryTabForm, UserTabForm
from django.utils import timezone
from django.contrib.auth.hashers import check_password

def index(request):
	return render(request, 'index.html')

def create_category(request):
	if request.method == 'POST':
		form = CategoryTabForm(request.POST, request.FILES)
		user_form = UserTabForm(request.POST)

		if form.is_valid() and user_form.is_valid():
			name = user_form.cleaned_data['name']
			password = user_form.cleaned_data['password']

			user_is_validated = validate_admin_user(request, name, password) 

			if user_is_validated != True:
				return user_is_validated

			form.save()
	else:
		form = CategoryTabForm()
		user_form = UserTabForm(request.POST)
		
	return render(request, 'upload.html', {
		'form': form,
		'user_form': user_form,
	})

def create_event_category(request):
	if request.method == 'POST':
		form = EventCategoryTabForm(request.POST, request.FILES)
		user_form = UserTabForm(request.POST)

		if form.is_valid() and user_form.is_valid():
			name = user_form.cleaned_data['name']
			password = user_form.cleaned_data['password']

			user_is_validated = validate_admin_user(request, name, password) 

			if user_is_validated != True:
				return user_is_validated

			form.save()

	else:
		form = EventCategoryTabForm()
		user_form = UserTabForm(request.POST)
		
	return render(request, 'upload.html', {
		'form': form,
		'user_form': user_form,
	})

def image_upload(request):
	if request.method == 'POST':
		form = ImageTabForm(request.POST, request.FILES)
		user_form = UserTabForm(request.POST)

		if form.is_valid() and user_form.is_valid():
			name = user_form.cleaned_data['name']
			password = user_form.cleaned_data['password']

			user_is_validated = validate_admin_user(request, name, password) 

			if user_is_validated != True:
				return user_is_validated

			form.save()
	else:
		form = ImageTabForm()
		user_form = UserTabForm(request.POST)

		
	return render(request, 'upload.html', {
		'form': form,
		'user_form': user_form,
	})

def create_event(request):
	if request.method == 'POST':
		event_form = EventTabForm(request.POST)
		user_form = UserTabForm(request.POST)

		if event_form.is_valid() and user_form.is_valid():
			name = user_form.cleaned_data['name']
			password = user_form.cleaned_data['password']

			user_is_validated = validate_admin_user(request, name, password) 

			if user_is_validated != True:
				return user_is_validated

			event = event_form.save()
	
	else:
		user_form = UserTabForm()
		event_form = EventTabForm()

	return render(request, 'upload.html', {
		'user_form': user_form,
		'form': event_form
   })

def validate_admin_user(request, name, password):
	users = UserTab.objects.filter(name=name)

	if not users.exists():
		return render(request, '../templates/error.html', {
			'error': "Unknown user"
		})

	user = users[0]

	if not check_password(password, user.password):
		return render(request, '../templates/error.html', {
			'error': "Invalid email or password"
		})

	if user.is_admin != 1:
		return render(request, '../templates/error.html', {
			'error': "Not admin"
		})

	return True