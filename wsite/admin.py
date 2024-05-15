from django.contrib import admin
from .models import  Question, Answer, Class, Subject, Category
# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Category)