from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import random
import qrcode
import os
from twilio.rest import Client
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.conf.urls.static import static
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Post, Profile, DeliveryPerson
from accounts.forms import PostForm, DeliveryPersonForm

from twilio.rest import TwilioRestClient
from django.conf import settings

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

otp = 0

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'base.html'

class HomePage(TemplateView):
    template_name = 'index.html'



class UserPage(TemplateView):
    template_name = 'user.html'

def Employee(request):
    return render(request, "blog/employee.html")


def Validateuser(request):
    rno = random.randint(100000,999999)
    global otp
    otp = rno
    im = qrcode.make("OTP is "+str(rno))
    print(otp)
    im.save(r"static/qrimages/qrcode.jpg")


    #account = "ACb4ca8e0c1bef94a8507dd2f9cabeb527"
    #token = "bc6683125ac1f284660a2d67291123bf"

    #client = Client(account, token)

    #message = client.messages.create(from_='+',to='+917061729810',
    #                         body="Text message you are sending to receiver")

    return render(request, "validate_login.html", )

def ValidateOTP(request):
    user_otp = request.POST.get("otp")
    print(user_otp)
    if user_otp == str(otp):
        return redirect('home')
    else:
    #    messages.warning(request, 'Please enter the correct OTP to login')
        return redirect('validate_login', {'messages':messages})

def delivery_person_view(request):


      name = request.user.username
      print(name)

      try:
          deliveryperson = DeliveryPerson.objects.get(user=name)
          print(deliveryperson.PhoneNo)
      except ObjectDoesNotExist:
          deliveryperson = 'None'
          return render(request, 'base.html')
      if deliveryperson != 'None':
          return render(request, 'base.html', {'deliveryperson': deliveryperson})


def download(request):
    return redirect('validate_login')


def index(request):
    return HttpResponse("Congrats, you're now logged in!")

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_staff:
                login(request,user)
                return HttpResponseRedirect(reverse('adminpage'))
            else:
                return HttpResponse("You are not an admin.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'admin.html', {})

class AdminPage(TemplateView):
    template_name = 'adminpage.html'
