
from django.contrib import admin
from .models import Users, Foods, Comment

# 注册模型到后台管理
admin.site.register(Users)
admin.site.register(Foods)
admin.site.register(Comment)