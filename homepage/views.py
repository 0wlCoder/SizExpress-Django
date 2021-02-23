from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return redirect("accounts/home")
