"""这个python文件就是admin管理页面，修改后无需makemigrations"""
from django.contrib import admin
# Register your models here.
from .models import Topic, Entry

admin.site.register(Topic) # 注册条目
admin.site.register(Entry)
