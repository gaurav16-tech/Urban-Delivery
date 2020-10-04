from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput,EmailInput,PasswordInput
from .models import Post, DeliveryPerson
import datetime
import decimal

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
import random
otp=0

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your first name'}))
    last_name = forms.CharField(max_length=100, help_text='Last Name', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your last name'}))
    email = forms.EmailField(max_length=150, help_text='Email', widget= forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Enter your email ID'}))
    password1 = forms.CharField(max_length=16, help_text='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password'}))
    password2 = forms.CharField(max_length=16, help_text='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password again for confirmation'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        pass


class PostForm(forms.ModelForm):
    Name = forms.CharField(max_length=100, help_text='Name', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Name'}))
    Address = forms.CharField(max_length=100, help_text='Address', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Address'}))
    City = forms.CharField(max_length=100, help_text='City', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your City Name'}))
    State = forms.CharField(max_length=100, help_text='State', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your State Name'}))
    Pincode = forms.IntegerField(help_text='Pincode', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pincode'}))
    MobileNumber = forms.IntegerField(help_text='Mobile Number', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}))
    ShipmentWeight = forms.IntegerField(help_text='ShipmentWeight', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Gross Weight of your parcel'}))
    Origin = forms.CharField(max_length=100, help_text='Pickup Location', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your PickUp Location Address'}))
    Destination = forms.CharField(max_length=100, help_text='Destination', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Drop Location Address'}))

    class Meta:
        model = Post
        fields = ('Name', 'Address', 'City', 'State', 'Pincode', 'MobileNumber', 'ShipmentWeight', 'Origin', 'Destination', 'Uploadimage')
        widgets = {
            'Totalamount': TextInput(attrs={'readonly':'readonly'})
        }

class DeliveryPersonForm(forms.ModelForm):
    user = forms.CharField(max_length=100, help_text='Username', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Username'}))
    PhoneNo = forms.IntegerField(help_text='MobileNumber', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Mobile Number'}))
    Address = forms.CharField(max_length=100, help_text='Address', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Address'}))
    City = forms.CharField(max_length=100, help_text='City', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your City Name'}))
    State = forms.CharField(max_length=100, help_text='State', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your State Name'}))
    Pincode = forms.IntegerField(help_text='Pincode', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pincode'}))
    picture = forms.FileField(help_text='Upload your image', widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DeliveryPerson
        fields = ('user', 'PhoneNo', 'Address', 'City', 'State', 'Pincode', 'picture')

class OTPAuthenticationForm(AuthenticationForm):
    otp = forms.CharField(required=False, widget=forms.PasswordInput)

    def clean(self):
        # Allow Django to detect can user log in
        super(OTPAuthenticationForm, self).clean()

        # If we got this far, we know that user can log in.
        if self.request.session.has_key('_otp'):
            if self.request.session['_otp'] != self.cleaned_data['otp']:
                raise forms.ValidationError("Invalid OTP.")
            del self.request.session['_otp']
        else:
            # There is no OTP so create one and send it by email
            otp = "1234"
            send_mail(
                subject="Your OTP Password",
                message="Your OTP password is %s" % otp,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["gk.helix16@gmail.com"]
            )
            self.request.session['_otp'] = otp
            # Now we trick form to be invalid
            raise forms.ValidationError("Enter OTP you received via e-mail")
