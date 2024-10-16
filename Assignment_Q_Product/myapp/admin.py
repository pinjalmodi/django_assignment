from django.contrib import admin
from .models import User,Product_mst,Product_sub_cat

# Register your models here.
admin.site.register(User)
admin.site.register(Product_mst)
admin.site.register(Product_sub_cat)
