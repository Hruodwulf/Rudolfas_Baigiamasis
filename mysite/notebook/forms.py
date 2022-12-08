from .models import Note, Category
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class UserNoteCreateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'picture']
        widgets = {'owner': forms.HiddenInput(), 'date_created':DateInput()}


class UserCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {'creator': forms.HiddenInput()}
