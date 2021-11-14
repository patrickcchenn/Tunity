from django.contrib import admin

# Register your models here.
from .models import User, company, vacancy,applied,condition,CV

admin.site.register(company)
admin.site.register(User)
admin.site.register(vacancy)
admin.site.register(applied)
admin.site.register(condition)
admin.site.register(CV)
