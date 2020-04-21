from django.shortcuts import render

# Create your views here.
def landingIndex(req):
    return render(req, 'landing/index.html')