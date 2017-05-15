from api.models import EventTab, UserTab, CategoryTab, LikeTab, CommentTab, RegistrationTab, EventCategoryTab

from django.utils import timezone
from django.contrib.auth.hashers import make_password
import datetime


def run():
	EventTab.objects.all().delete()
	UserTab.objects.all().delete()
	CategoryTab.objects.all().delete()
	CommentTab.objects.all().delete()
	RegistrationTab.objects.all().delete()
	LikeTab.objects.all().delete()
	EventCategoryTab.objects.all().delete()

	now = timezone.now()
	end = now + datetime.timedelta(days=1)

	# Create 5 events
	event1 = EventTab(title="Garena Event1", description="Test1", create_time=now.strftime('%s'), start_date=now.strftime('%s'), end_date=end.strftime('%s'), latitude=1.300981, longitude=103.788636)
	event2 = EventTab(title="Garena Event2", description="Test2", create_time=now.strftime('%s'), start_date=now.strftime('%s'), end_date=end.strftime('%s'), latitude=1.300981, longitude=103.788636)
	event3 = EventTab(title="Garena Event3", description="Test3", create_time=now.strftime('%s'), start_date=now.strftime('%s'), end_date=end.strftime('%s'), latitude=1.300981, longitude=103.788636)
	event4 = EventTab(title="Garena Event4", description="Test4", create_time=now.strftime('%s'), start_date=now.strftime('%s'), end_date=end.strftime('%s'), latitude=1.300981, longitude=103.788636)
	event5 = EventTab(title="Garena Event5", description="Test5", create_time=now.strftime('%s'), start_date=now.strftime('%s'), end_date=end.strftime('%s'), latitude=1.300981, longitude=103.788636)

	event1.save()
	event2.save()
	event3.save()
	event4.save()
	event5.save()

	# Create 5 admin users
	user1 = UserTab(name="superuser1", email="fakeemail1@gmail.com", is_admin=1, password=make_password("Garena.com"), create_time=now.strftime("%s"))
	user2 = UserTab(name="superuser2", email="fakeemail2@gmail.com", is_admin=1, password=make_password("Garena.com"), create_time=now.strftime("%s"))
	user3 = UserTab(name="superuser3", email="fakeemail3@gmail.com", is_admin=1, password=make_password("Garena.com"), create_time=now.strftime("%s"))
	user4 = UserTab(name="superuser4", email="fakeemail4@gmail.com", is_admin=1, password=make_password("Garena.com"), create_time=now.strftime("%s"))
	user5 = UserTab(name="superuser5", email="fakeemail5@gmail.com", is_admin=1, password=make_password("Garena.com"), create_time=now.strftime("%s"))

	user1.save()
	user2.save()
	user3.save()
	user4.save()
	user5.save()

	# Create 3 likes for each user to each event
	like1 = LikeTab(user_id=user1.id, event_id=event1.id)
	like2 = LikeTab(user_id=user2.id, event_id=event2.id)
	like3 = LikeTab(user_id=user3.id, event_id=event1.id)

	like1.save()
	like2.save()
	like3.save()

	# Create 3 comments
	comment1 = CommentTab(user_id=user1.id, event_id=event1.id, description="I am excited for this event")
	comment2 = CommentTab(user_id=user1.id, event_id=event1.id, description="This event is not fun")
	comment3 = CommentTab(user_id=user2.id, event_id=event2.id, description="I am excited for this event")

	comment1.save()
	comment2.save()
	comment3.save()

	# Create 3 registration
	registration1 = RegistrationTab(user_id=user1.id, event_id=event1.id)
	registration2 = RegistrationTab(user_id=user2.id, event_id=event2.id)
	registration3 = RegistrationTab(user_id=user3.id, event_id=event1.id)

	registration1.save()
	registration2.save()
	registration3.save()

	# Create categories
	category1 = CategoryTab(name="Music")
	category2 = CategoryTab(name="Soccer")
	category3 = CategoryTab(name="Mathematics")
	category4 = CategoryTab(name="Artificial Intelligence Meetup")
	category5 = CategoryTab(name="Web Developers")

	category1.save()
	category2.save()
	category3.save()
	category4.save()
	category5.save()

	# Link Categories
	event_category1 = EventCategoryTab(event_id=event1.id, category_id=category1.id)
	event_category2 = EventCategoryTab(event_id=event2.id, category_id=category2.id)
	event_category3 = EventCategoryTab(event_id=event3.id, category_id=category3.id)
	event_category4 = EventCategoryTab(event_id=event4.id, category_id=category4.id)
	event_category5 = EventCategoryTab(event_id=event4.id, category_id=category5.id)
	event_category6 = EventCategoryTab(event_id=event5.id, category_id=category5.id)

	event_category1.save()
	event_category2.save()
	event_category3.save()
	event_category5.save()
	event_category4.save()
	event_category6.save()