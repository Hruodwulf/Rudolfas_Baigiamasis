from django.contrib import admin
from . models import Note, Category

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'date_created', 'picture')
    list_filter = ('owner', 'date_created')
    list_editable = ('owner', 'picture')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')
    list_filter = ('name', 'creator')
    list_editable = ['creator']

admin.site.register(Note, NoteAdmin)
admin.site.register(Category, CategoryAdmin)
