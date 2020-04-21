import time

import pytesseract
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import ClockInForm
from .utils import getCode
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url="/login")
def appIndex(req):
    return redirect("app:appDashboard")


@login_required(login_url="/login")
def appDashboard(req):
    user = req.user
    if user.is_authenticated:
        if user.is_superuser:

            allUsers = User.objects.all()
            table = {}
            for i in allUsers:
                clockedIn = True
                try:
                    i.timecard_set.get(completed=False)
                    clockedIn = True
                except ObjectDoesNotExist:
                    clockedIn = False

                timeCard = None
                if not clockedIn:
                    # Get last clockin
                    if(len(i.timecard_set.order_by('-timeOut')) > 0):
                        timeCard = i.timecard_set.order_by('-timeOut')[0]
                    else:
                        timeCard = None

                else:
                    timeCard = i.timecard_set.get(completed=False)

                table[i.username] = {
                    'name': i.get_full_name(),
                    'timeCard': timeCard,
                    'clockedIn': clockedIn,
                }

            return render(req, 'app/dashboardSU.html', {'user': user, 'table': table})


        else:
            clockedIn = False
            try:
                user.timecard_set.get(completed=False)
                clockedIn = True
            except ObjectDoesNotExist:
                clockedIn = False

            remakeCode = True
            userCodes = user.verificationcode_set.all()
            if len(userCodes) == 1:
                codeObj = userCodes[0]
                if codeObj.expiryDate < timezone.now():
                    # Code expired
                    remakeCode = True
                else:
                    remakeCode = False
            elif len(userCodes) > 1:
                # This should never happen!
                remakeCode = True
            else:
                remakeCode = True

            code = ""
            if (remakeCode == True):
                code = getCode()
                user.verificationcode_set.all().delete()
                user.verificationcode_set.create(code=code, expiryDate=timezone.now() + timezone.timedelta(minutes=5))
            else:
                code = user.verificationcode_set.all()[0].code
            form = ClockInForm()
            return render(req, 'app/dashboardNormal.html',
                          {'user': user, 'clockedIn': clockedIn, 'code': code, 'form': form})


@login_required(login_url="/login")
def appClockIn(req):
    if req.method == "POST":
        clockedIn = False
        try:
            req.user.timecard_set.get(completed=False)
            clockedIn = True
        except ObjectDoesNotExist:
            clockedIn = False
        if(clockedIn == False):

            user = req.user
            userCodes = user.verificationcode_set.all()
            if len(userCodes) == 1:
                codeObj = userCodes[0]
                if codeObj.expiryDate > timezone.now():

                    form = ClockInForm(req.POST, req.FILES)
                    if form.is_valid():
                        file = req.FILES['file']
                        print(file.name)
                        if file.name.endswith(".jpg") or file.name.endswith(".png"):
                            ocr = processFile(file)
                            if ocr == codeObj.code:

                                user.timecard_set.create(timeIn=timezone.now())


                                return redirect("app:appIndex")
                            else:
                                return HttpResponse("Wrong Code, correct code is "+codeObj.code+", provided "+ocr)
                        else:
                            return HttpResponse("Incorrect file")
                    else:
                        return HttpResponse("Incorrect file")
                else:
                    return HttpResponse("Code Expired")
            else:
                return HttpResponse("Code Expired")
        else:
            return redirect("app:appIndex")


def processFile(file):
    fileName = 'tmp/' + str(time.time()) + "." + file.name.split(".")[-1]
    with open(fileName, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        return pytesseract.image_to_string(Image.open(fileName), lang="eng", config="--psm 12  --oem 2")

@login_required(login_url="/login")
def appClockOut(req):
    if req.method == "POST":
        clockedIn = False
        try:
            req.user.timecard_set.get(completed=False)
            clockedIn = True
        except ObjectDoesNotExist:
            clockedIn = False
        if(clockedIn == True):
            timecard = req.user.timecard_set.get(completed=False)
            timecard.completed = True
            timecard.timeOut = timezone.now()
            timecard.save()
            return redirect("app:appIndex")