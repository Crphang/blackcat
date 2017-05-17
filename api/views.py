from api.models import EventTab, UserTab, CategoryTab, LikeTab, CommentTab, RegistrationTab, EventCategoryTab
from api.helper import get_user_by_id, is_login

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

import json
import jwt
import os

EXPIRY_DURATION = 86400000
SECRET_KEY = os.environ['SECRET_KEY']


def index(request):
    return HttpResponse("Api Home")


@is_login
def event_index(request, user):
	events = EventTab.objects.all()
	response = {}
	for event in events:
		response[event.id] = dict(event.to_dict().items() + {
			'participants_count': RegistrationTab.objects.filter(event_id=event.id).count(),
			'likes_count': LikeTab.objects.filter(event_id=event.id).count(),
			'comments_count': LikeTab.objects.filter(event_id=event.id).count()
		}.items())

	return HttpResponse(json.dumps(response), content_type='Application/Json')


@is_login
def event_detail(request, user):
	event_id = request.GET['event_id']
	event = EventTab.objects.filter(id=event_id)

	if not event.exists():
		return HttpResponse("No event")

	participants = map(lambda x: get_user_by_id(x.user_id), RegistrationTab.objects.filter(event_id=event_id))
	likes = map(lambda x: get_user_by_id(x.user_id), LikeTab.objects.filter(event_id=event_id))
	comments = map(lambda x: {"user": get_user_by_id(x.user_id), "comment": x.description}, CommentTab.objects.filter(event_id=event_id))

	event = event.first()
	response = dict(
		{
			'likes': likes,
			'comments': comments,
			'participants': participants,
		}.items() + event.to_dict().items())

	return HttpResponse(json.dumps(response), content_type='Application/Json')


@csrf_exempt
@is_login
def like(request, user):
	payload = json.loads(request.body)
	user_id = payload['user_id']
	event_id = payload['event_id']
	like = LikeTab.filter(user_id=user_id, event_id=event_id)
	if like.exists():
		return HttpResponse(json.dumps({"error": "Already Liked"}), status=200)

	like = LikeTab(user_id=user_id, event_id=event_id)
	like.save()
	return HttpResponse(content_type='Application/Json', status=200)


@csrf_exempt
@is_login
def comment(request, user):
	payload = json.loads(request.body)
	user_id = payload['user_id']
	event_id = payload['event_id']
	comment_description = payload['description']

	comment = Comment(user_id=user_id, event_id=event_id, description=comment_description)
	comment.save()
	return HttpResponse(content_type='Application/Json', status=200)


@csrf_exempt
@is_login
def register(request, user):
	payload = json.loads(request.body)
	user_id = payload['user_id']
	event_id = payload['event_id']
	registration = RegistrationTab.filter(user_id=user_id, event_id=event_id)
	if registration.exists():
		return HttpResponse(json.dumps({"error": "Already Liked"}), status=200)

	registration = RegistrationTab(user_id=user_id, event_id=event_id)
	registration.save()
	return HttpResponse(content_type='Application/Json', status=200)


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
		participating_events['participating_events'].update({event['id']: event})

	liked_events_id = LikeTab.objects.filter(user_id=user.id)
	liked_events = {'liked_events': {}}
	for like in liked_events_id:
		event = EventTab.objects.get(id=like.event_id).to_dict()
		liked_events['liked_events'].update({event['id']: event})

	response = dict(user.to_dict().items() + {"access_token": access_token}.items() + participating_events.items() + liked_events.items())

	return HttpResponse(json.dumps(response), content_type='Application/Json')


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
