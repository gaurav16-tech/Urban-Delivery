from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView)
from accounts.forms import ContactForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .tokens import account_activation_token
from django.conf import settings
from django.core.mail import send_mail, EmailMessage

from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework import status
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from .models import Post, Profile, DeliveryPerson
from .forms import PostForm, DeliveryPersonForm

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.conf.urls.static import static
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import F

class AboutView(TemplateView):
    template_name = 'about.html'

class DetailView(TemplateView):
    template_name = 'contact.html'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self,form):
        form.send_email()
        return super().form_valid(form)

def activation_sent_view(request):
    return render(request, 'activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_invalid.html')

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        subject, message, to=[to_email]
            )
            email.send()
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device
class TOTPCreateView(views.APIView):
    """
    Use this endpoint to set up a new TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED,)

class TOTPVerifyView(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, token, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device == None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            return Response(True, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

def post_new(request):
    saved = False
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            saved = True
            return redirect('/thanks/')

    else:
        form = PostForm()

    return render(request, 'blog/newpost.html', {'form': form})



def SaveProfile(request):
   saved = False

   if request.method == "POST":
      #Get the posted form
      MyProfileForm = DeliveryPersonForm(request.POST, request.FILES)

      if MyProfileForm.is_valid():

         MyProfileForm.save()
         saved = True
         return redirect('/thanks/')
   else:
      MyProfileForm = DeliveryPersonForm()

   return render(request, 'blog/profile.html', {'MyProfileForm': MyProfileForm})


def PostDetailView(request, pk):
    post = get_object_or_404(Post,pk=pk)


    return render(request, 'blog/postdetail.html', {'post': post})

def post_detail_view(request):


      name = request.user.username
      print(name)

      try:
          DP = DeliveryPerson.objects.get(user=name)
          print(DP.PhoneNo)
      except ObjectDoesNotExist:
          DP = 'None'

      if DP == 'None':
          posts = Post.objects.filter(Name=name).order_by('created_date')
          return render(request, 'blog/postlist.html', {'posts': posts, 'DP': DP})
      else:
          open = 1
          ID = DeliveryPerson.objects.get(user=name)
          print(ID)

          posts = Post.objects.filter(Status=open, deliveryperson=ID).order_by('created_date')
          return render(request, 'blog/postlist.html', {'posts': posts})


def calculate_amount_view(request):
    amount = 0
    post = Post.objects.get(Status="OPEN")
    post.Totalamount = F('Totalamount') + 100.00
    post.save(update_fields=["Totalamount"])
    Amnt = Post.objects.get(Status="OPEN")
    amount = Amnt.Totalamount
    return render(request, 'blog/post_edit.html', {'amount': amount})
