from django.contrib import admin
from .models import User, Vehicle, Ads, Address

# Register your models here.
admin.site.register(User)
admin.site.register(Vehicle)
admin.site.register(Ads)
admin.site.register(Address)
