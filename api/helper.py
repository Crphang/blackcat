from api.models import UserTab
from django.http import HttpResponse
from django.utils import timezone

import json
import jwt
import os

SECRET_KEY = os.environ['SECRET_KEY']


def get_user_by_id(id):
	user = UserTab.objects.filter(id=id)
	if not user.exists():
		return None

	user = user.first()
	return user.to_dict()


def is_login(end_point):

	def wrapper(request):
		access_token = request.META['HTTP_X_AUTH_TOKEN']
		payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])

		if not payload['id']:
			return HttpResponse(json.dumps({"error": "Not Logined"}), status=200)

		users = UserTab.objects.filter(id=payload['id'])

		if not users.exists():
			return HttpResponse(json.dumps({"error": "Not Logined"}), status=200)

		user = users.first()
		# Check Token
		if user.access_token != access_token:
			return HttpResponse(json.dumps({"error": "Not Logined"}), status=200)

		# Check Expiry
		now = int(timezone.now().strftime('%s'))
		if not payload['expiry_date'] or now > payload['expiry_date']:
			return HttpResponse(json.dumps({"error": "Not Logined"}), status=200)

		return end_point(request, user)

	return wrapper
