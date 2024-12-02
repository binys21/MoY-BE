from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Black)
class BlackAdmin(admin.ModelAdmin):
	list_display = ['id','category', 'name','description','information','color','frame']
	list_display_links = ['id','name']
	
@admin.register(White)
class BlackAdmin(admin.ModelAdmin):
	list_display = ['id','category', 'name','description','color','frame']
	list_display_links = ['id','name']
