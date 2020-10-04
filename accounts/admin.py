from django.contrib import admin
from .models import Profile
from accounts.models import Post, DeliveryPerson

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(DeliveryPerson)
# Register your models here.
