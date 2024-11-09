from django.contrib import admin
from .models import MyModel
from .forms import MyModelForm

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    form = MyModelForm
