from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from .models import Note, Category
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import UserNoteCreateForm, UserCategoryCreateForm


# Create your views here.

def index(request):
    return render(request, 'notebook/index.html')

class NoteListView(LoginRequiredMixin, generic.ListView):
    model = Note
    template_name = 'notebook/note_list.html'
    context_object_name = 'mynotes'

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Note
    template_name = 'notebook/note_detail'

    def get_success_url(self):
        return reverse('note_detail', kwargs={'pk': self.object.id})

class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'notebook/category_list.html'
    context_object_name = 'mycategory'

    def get_queryset(self):
        return Category.objects.filter(creator=self.request.user)

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Category
    template_name = 'notebook/category_detail'

    def get_success_url(self):
        return reverse('category_detail', kwargs={'pk': self.object.id})


def search(request):
    query = request.GET.get('query')
    lt_letters = {'ž': 'z', 'š': 's', 'į':'i'}
    for letter in query:
       if letter in lt_letters.keys():
           print(lt_letters[letter])
    search_results = Note.objects.filter(Q(title__icontains=query) | Q(summary__icontains = query))
    return render(request, 'notebook/search.html', {'mynotes': search_results, 'query': query})

class NoteByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Note
    success_url = '/mynotes/'
    template_name = 'notebook/user_note_form.html'
    form_class = UserNoteCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

class NoteByUserUpdateView(LoginRequiredMixin, generic.UpdateView, UserPassesTestMixin):
    model = Note
    fields = ['title', 'content', 'category', 'picture']
    success_url = '/mynotes/'
    template_name = 'notebook/user_note_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)
    def test_func(self):
        note = self.get_object()
        return self.request.user == note.owner

class CategoryByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    success_url = '/mycategory/'
    template_name = 'notebook/user_category_form.html'
    form_class = UserCategoryCreateForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return super().form_valid(form)

class CategoryByUserUpdateView(LoginRequiredMixin, generic.UpdateView, UserPassesTestMixin):
    model = Category
    fields = ['name']
    success_url = '/mycategory/'
    template_name = 'notebook/user_category_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return super().form_valid(form)
    def test_func(self):
        category = self.get_object()
        return self.request.user == category.creator

class NoteByUserDeleteView(generic.DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Note
    success_url = '/mynotes/'
    template_name = 'notebook/note_delete.html'
    context_object_name = 'note'

    def test_func(self):
        note = self.get_object()
        return note.owner == self.request.user

class CategoryByUserDeleteView(generic.DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Category
    success_url = '/mycategory/'
    template_name = 'notebook/category_delete.html'
    context_object_name = 'category'

    def test_func(self):
        category = self.get_object()
        return category.creator == self.request.user

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST ['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, _('Username %s already exists!') % username)
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, _('Username with %s already exists!') % email)
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    return render(request, 'notebook/index.html')
        else:
            messages.error(request, _('Passwords do no match!'))
            return redirect('register')
    return render(request, 'notebook/register.html')
