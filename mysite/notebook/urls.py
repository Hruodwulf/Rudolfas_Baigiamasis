from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('mynotes/', views.NoteListView.as_view(), name='note-list'),
    path('mycategory/', views.CategoryListView.as_view(), name='category-list'),
    path('mynotes/<int:pk>', views.NoteDetailView.as_view(), name='note-detail'),
    path('mycategory/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('mynotes/newnote', views.NoteByUserCreateView.as_view(), name='new-note'),
    path('mycategory/newcat', views.CategoryByUserCreateView.as_view(), name='new-category'),
    path('mynotes/<int:pk>/update', views.NoteByUserUpdateView.as_view(), name='note-update'),
    path('mycategory/<int:pk>/update', views.CategoryByUserUpdateView.as_view(), name='category-update'),
    path('mynotes/<int:pk>/delete', views.NoteByUserDeleteView.as_view(), name='note-delete'),
    path('mycategory/<int:pk>/delete', views.CategoryByUserDeleteView.as_view(), name='category-delete'),
]
