from django.forms import widgets
from . models import *
class DashboardForm(forms.form):
    text=forms.Charfield(max_length=100,lable="Enter your search")