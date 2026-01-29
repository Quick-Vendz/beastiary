from django.contrib import admin
from django import forms
from .models import *

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('index', 'title', 'slug')
    search_fields = ('title',)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('index', 'title', 'book', 'slug')
    list_filter = ('book',)
    search_fields = ('title',)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('index', 'title', 'book', 'chapter', 'parent')
    list_filter = ('book', 'chapter')
    search_fields = ('title', 'content')
    
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 30, 'cols': 100})},
    }
