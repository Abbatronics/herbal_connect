from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=False)  # Make username optional
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        
        if not username and not email:
            raise ValidationError("You must provide either username or email")
            
        if username and User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
            
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered")
            
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.username:
            user.username = user.email  # Use email as username if not provided
        if commit:
            user.save()
        return user