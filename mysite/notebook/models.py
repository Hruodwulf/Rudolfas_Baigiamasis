from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import date

# Create your models here.

class Category(models.Model):
    name = models.CharField('Pavadinimas', max_length=100, help_text='Nurodykite kategorijos pavadinimą')
    creator = models.ForeignKey(User,  on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategorija'
        verbose_name_plural = 'Kategorijos'

class Note(models.Model):
    title = models.CharField('Pavadinimas', max_length=100, help_text='Užrašo pavadinimas')
    owner = models.ForeignKey(User,  on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField('Užrašo turinys', max_length=1000, help_text='Čia rašykite norimą išsaugoti informaciją')
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, help_text='Pasirinkite įrašo kategorijas')
    picture = models.ImageField(default='default.png', upload_to='note_pics')

    def __str__(self):
        return self.title

    def display_category(self):
        return ','.join(category.name for category in self.category.all()[:3])

    class Meta:
        verbose_name = 'Užrašas'
        verbose_name_plural = 'Užrašai'
