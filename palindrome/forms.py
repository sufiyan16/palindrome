from django.forms import ModelForm
from .models import Palindrome

class PalindromeForm(ModelForm):
    class Meta:
        model=Palindrome
        fields= ['input']