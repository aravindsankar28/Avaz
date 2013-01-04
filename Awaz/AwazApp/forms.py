from django import forms
from AwazApp.models import ImageUpload
        
class ImageUploadForm(forms.ModelForm):
	class Meta:
		model = ImageUpload

class SearchImageForm(forms.Form):
	search_field = forms.CharField(max_length=40)
	
	
