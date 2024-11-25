from django import forms
from .models import MyModel

class MyModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = MyModel
        fields = '__all__'
