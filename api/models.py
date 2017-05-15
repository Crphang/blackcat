from django.db import models

# Create your models here.


class UserTab(models.Model):
	id = models.AutoField(primary_key=True)
	create_time = models.PositiveIntegerField()
	access_token = models.CharField(max_length=1024)
	email = models.CharField(max_length=256)
	name = models.CharField(max_length=64)
	password = models.CharField(max_length=256)
	is_admin = models.IntegerField()

	def to_dict(self):
		return({
			'email': self.email,
			'create_time': self.create_time,
			'name': self.name,
			'is_admin': self.is_admin
		})

	class Config:
		db_for_write = 'black_cat_db.write'
		db_for_read = 'black_cat_db.read'

	class Meta:
		db_table = u'user_tab'


class EventTab(models.Model):
	id = models.AutoField(primary_key=True)
	create_time = models.PositiveIntegerField()
	start_date = models.PositiveIntegerField()
	end_date = models.PositiveIntegerField()
	title = models.CharField(max_length=64)
	latitude = models.FloatField(6, max_length=10)
	longitude = models.FloatField(6, max_length=10)
	description = models.TextField()

	def to_dict(self):
		return ({
			'id': self.id,
			'create_time': self.create_time,
			'start_date': self.start_date,
			'end_date': self.end_date,
			'title': self.title,
			'latitude': self.latitude,
			'longitude': self.longitude,
			'description': self.description
		})

	class Config:
		db_for_write = 'black_cat_db.write'
		db_for_read = 'black_cat_db.read'

	class Meta:
		db_table = u'event_tab'


class ImageTab(models.Model):
	id = models.AutoField(primary_key=True)
	event_id = models.PositiveIntegerField()
	url = models.CharField(max_length=256)

	class Config:
		db_for_write = 'black_cat_db.write'
		db_for_read = 'black_cat_db.read'

	class Meta:
		db_table = u'image_tab'


class CategoryTab(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name
		}

	class Config:
		db_for_write = 'black_cat_db.write'
		db_for_read = 'black_cat_db.read'

	class Meta:
		db_table = u'category_tab'


class RegistrationTab(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.PositiveIntegerField()
	event_id = models.PositiveIntegerField()

	class Config:
		db_for_write = 'black_cat_db.write'
		db_for_read = 'black_cat_db.read'

	class Meta:
		db_table = u'registration_tab'
		unique_together = (("user_id", "event_id"),)


class CommentTab(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.PositiveIntegerField()
	event_id = models.PositiveIntegerField()
	description = models.TextField()

	class Config:
		db_for_write = 'black_cat_db.write'
		db_for_read = 'black_cat_db.read'

	class Meta:
		db_table = u'comment_tab'


class LikeTab(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.PositiveIntegerField()
	event_id = models.PositiveIntegerField()

	class Config:
		db_for_write = 'black_cat_db.write'
		db_for_read = 'black_cat_db.read'

	class Meta:
		db_table = u'like_tab'
		unique_together = (("user_id", "event_id"),)


class EventCategoryTab(models.Model):
	id = models.AutoField(primary_key=True)
	category_id = models.PositiveIntegerField()
	event_id = models.PositiveIntegerField()

	class Config:
		db_for_write = 'black_cat_db.write'
		db_for_read = 'black_cat_db.read'

	class Meta:
		db_table = u'event_category_tab'
		unique_together = (("category_id", "event_id"),)
