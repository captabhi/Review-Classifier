from django import forms
from .models import Review,Old_Training_data,Training_Review
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    username=forms.CharField
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','password']

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        exclude=['item','timestamp','review_type','is_verified']


class AdminReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        exclude=['item','timestamp']
class Training_ReviewForm(forms.ModelForm):
    class Meta:
        model=Training_Review
        exclude=[]

class Old_Form(forms.ModelForm):
    class Meta:
        model=Old_Training_data
        exclude=[]