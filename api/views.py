from api.models import EventTab, UserTab, CategoryTab, LikeTab, CommentTab, RegistrationTab, EventCategoryTab, ImageTab
from api.helper import get_user_by_id, is_login

from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.middleware.csrf import get_token

import json
import jwt
import os

EXPIRY_DURATION = 86400000
SECRET_KEY = os.environ['SECRET_KEY']


def index(request):
    return HttpResponse("Api Home")


@is_login
def event_index(request, user):
	page = request.GET.get('page_count')
	start_date_milliseconds = int(request.GET.get('start_date'))
	end_date_milliseconds = int(request.GET.get('end_date'))
	category = request.GET.get('category')

	start_date_seconds = start_date_milliseconds / 1000
	end_date_seconds = end_date_milliseconds / 1000

	if category == 'All':
		events = EventTab.objects.filter(start_date__gte=start_date_seconds, end_date__lte=end_date_seconds).order_by('id')
	else:
		event_ids_with_category = map(lambda x: EventTab.objects.get(id=x.event_id).id, EventCategoryTab.objects.filter(category_id=category))
		events = EventTab.objects.filter(id__in=event_ids_with_category).filter(start_date__gte=start_date_seconds, end_date__lte=end_date_seconds).order_by('id')

	paginator = Paginator(events, 5)


	try:
		events = paginator.page(page)
	except PageNotAnInteger:
		page = 1
		events = paginator.page(1)
	except EmptyPage:
		page = 1
		events = paginator.page(1)
	response = {}
	for event in events:
		event_category = EventCategoryTab.objects.filter(event_id=event.id)
		if event_category.exists():
			category = CategoryTab.objects.get(id=event_category[0].category_id)
			response[event.id] = dict(event.to_dict().items() + {
				'participants_count': RegistrationTab.objects.filter(event_id=event.id).count(),
				'likes_count': LikeTab.objects.filter(event_id=event.id).count(),
				'page_count': page,
				'category': category.to_dict()
			}.items())	
		else:
			response[event.id] = dict(event.to_dict().items() + {
				'participants_count': RegistrationTab.objects.filter(event_id=event.id).count(),
				'likes_count': LikeTab.objects.filter(event_id=event.id).count(),
				'page_count': page,
			}.items())
	response['total_pages'] = paginator.num_pages

	return HttpResponse(json.dumps(response), content_type='Application/Json')


@is_login
def event_detail(request, user):
	event_id = request.GET['event_id']
	event = EventTab.objects.filter(id=event_id)

	if not event.exists():
		return HttpResponse("No event")

	participants = map(lambda x: get_user_by_id(x.user_id), RegistrationTab.objects.filter(event_id=event_id))
	likes = map(lambda x: get_user_by_id(x.user_id), LikeTab.objects.filter(event_id=event_id))
	comments = map(lambda x: {"user": get_user_by_id(x.user_id), "comment": x.description, "time": x.create_time}, CommentTab.objects.filter(event_id=event_id))
	images = map(lambda x: x.file.url, ImageTab.objects.filter(event_id=event_id))
	event = event.first()
	response = dict(
		{
			'likes': likes,
			'comments': comments,
			'participants': participants,
			'images': images,
		}.items() + event.to_dict().items())

	return HttpResponse(json.dumps(response), content_type='Application/Json')

@is_login
def like(request, user):
	payload = json.loads(request.body)
	event_id = payload['event_id']
	like = LikeTab.objects.filter(user_id=user.id, event_id=event_id)
	if like.exists():
		return HttpResponse(json.dumps({"error": "Already Liked"}), status=200)

	like = LikeTab(user_id=user.id, event_id=event_id)
	like.save()

	event = EventTab.objects.get(id=event_id).to_dict()
	return HttpResponse(json.dumps(event), content_type='Application/Json', status=200)

@is_login
def comment(request, user):
	payload = json.loads(request.body)
	event_id = payload['event_id']
	comment_description = payload['description']

	now = int(timezone.now().strftime('%s'))
	comment = CommentTab(user_id=user.id, event_id=event_id, description=comment_description, create_time=now)
	comment.save()

	new_comment = {"user": get_user_by_id(comment.user_id), "event_id": comment.event_id, "comment": comment.description, "time": comment.create_time}

	return HttpResponse(json.dumps(new_comment), content_type='Application/Json', status=200)


@is_login
def register(request, user):
	payload = json.loads(request.body)
	print(payload)
	event_id = payload['event_id']
	registration = RegistrationTab.objects.filter(user_id=user.id, event_id=event_id)
	if registration.exists():
		return HttpResponse(json.dumps({"error": "Already Registered"}), status=200)

	registration = RegistrationTab(user_id=user.id, event_id=event_id)
	registration.save()

	event = EventTab.objects.get(id=event_id).to_dict()
	return HttpResponse(json.dumps(event), content_type='Application/Json', status=200)


@csrf_exempt
def login(request):
	print request.body
	payload = json.loads(request.body)
	print(payload)
	username = payload['username']
	password = payload['password']

	users = UserTab.objects.filter(name=username)
	if not users.exists():
		return HttpResponse(json.dumps({"error": "Invalid Username or Password"}), status=200)

	user = users.first()
	if not check_password(password, user.password):
		return HttpResponse(json.dumps({"error": "Invalid Username or Password"}), status=200)

	# Generate Access Token
	expiry_date = int(timezone.now().strftime('%s')) + EXPIRY_DURATION
	access_token = jwt.encode({'id': user.id, 'expiry_date': expiry_date}, SECRET_KEY, algorithm='HS256')

	user.access_token = access_token
	user.save()

	participating_events_id = RegistrationTab.objects.filter(user_id=user.id)
	participating_events = {'participating_events': {}}
	for reg in participating_events_id:
		event = EventTab.objects.get(id=reg.event_id).to_dict()
		event_category = EventCategoryTab.objects.filter(event_id=event['id'])
		if event_category.exists():
			category = CategoryTab.objects.get(id=event_category[0].category_id)
			event = dict({
				'category': category.to_dict(),
				}.items() + event.items())
		participating_events['participating_events'].update({event['id']: event})

	liked_events_id = LikeTab.objects.filter(user_id=user.id)
	liked_events = {'liked_events': {}}
	for like in liked_events_id:
		event = EventTab.objects.get(id=like.event_id).to_dict()
		event_category = EventCategoryTab.objects.filter(event_id=event['id'])
		if event_category.exists():
			category = CategoryTab.objects.get(id=event_category[0].category_id)
			event = dict({
				'category': category.to_dict(),
				}.items() + event.items())
		liked_events['liked_events'].update({event['id']: event})

	response = dict(user.to_dict().items() + {"access_token": access_token}.items() + participating_events.items() + liked_events.items())
	response['X-CSRFToken'] = get_token(request)

	response = HttpResponse(json.dumps(response), content_type='Application/Json')
	
	return response


@csrf_exempt
@is_login
def logout(request, user):
	# Delete Access Token
	user.access_token = None
	user.save()

	return HttpResponse(content_type='Application/Json', status=200)


@is_login
def categories_index(request, user):
	categories = CategoryTab.objects.all()

	response = map(lambda category: category.to_dict(), categories)
	return HttpResponse(json.dumps(response), content_type='Application/Json')
