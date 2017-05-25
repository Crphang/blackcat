from django import forms
from api.models import ImageTab, EventTab, CategoryTab, EventCategoryTab, UserTab

class ImageTabForm(forms.ModelForm):
    class Meta:
        model = ImageTab
        fields = ('file', 'event_id', )

class ImageForm(forms.ModelForm):

    class Meta:
        model = ImageTab
        fields = ('file', )


class EventTabForm(forms.ModelForm):
	class Meta:
		model = EventTab
		fields = ('title', 'description', 'latitude', 'longitude', 'start_date', 'end_date', 'create_time', )

class CategoryTabForm(forms.ModelForm):
	class Meta:
		model = CategoryTab
		fields = ('name', )

class EventCategoryTabForm(forms.ModelForm):
	class Meta:
		model = EventCategoryTab
		fields = ('category_id', 'event_id',)

class UserTabForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = UserTab
		fields = ('name', 'password', )
