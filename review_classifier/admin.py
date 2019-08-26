from django.contrib import admin
from .models import Item
from .models import Review,Old_Training_data
# Register your models here.

admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Old_Training_data)