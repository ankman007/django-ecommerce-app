from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Please enter a valid address.")
    
    class Meta(UserCreationForm.Meta):
        model = User 
        fields = UserCreationForm.Meta.fields + ('email')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__isexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email