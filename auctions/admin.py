from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Created_by)