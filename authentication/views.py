from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, response
from django.shortcuts import render, redirect


# Create your views here.
def loginIndex(req):
    if req.method == "POST":
        form = AuthenticationForm(data=req.POST)
        if form.is_valid():
            user = form.get_user()
            login(req, user)
            return redirect("app:appIndex")
        else:
            return redirect("authorisation:loginIndex")
    else:
        form = AuthenticationForm()
        return render(req, "authentication/login.html", {'form': form})
