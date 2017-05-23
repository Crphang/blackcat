from django import forms
from api.models import ImageTab, EventTab, CategoryTab, EventCategoryTab

class ImageTabForm(forms.ModelForm):
    class Meta:
        model = ImageTab
        fields = ('file', 'event_id', )

class EventTabForm(forms.ModelForm):
	class Meta:
		model = EventTab
		fields = ('title', 'description', 'latitude', 'longitude', 'start_date', 'end_date', 'create_time', )

class CategoryTabForm(forms.ModelForm):
	class Meta:
		model = CategoryTab
		fields = ('name', )

class EventCategoryTab(forms.ModelForm):
	class Meta:
		model = EventCategoryTab
		fields = ('category_id', 'event_id',)