from django.contrib import admin
from .models import trade, stock,UserSettings


# Register your models here.
admin.site.register(trade)
admin.site.register(stock)
admin.site.register(UserSettings)
