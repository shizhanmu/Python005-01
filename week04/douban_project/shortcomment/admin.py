from django.contrib import admin
from .models import Short

# Register your models here.

class ShortAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'subject_id',
                    'title',
                    'rating',
                    'shorttext',
                    'nickname',
                    'category',
                    'posttime')
    
admin.site.register(Short, ShortAdmin)