from django import forms
from .models import User
#DataFlair #File_Upload
class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = [
        'profile_image',
        ]