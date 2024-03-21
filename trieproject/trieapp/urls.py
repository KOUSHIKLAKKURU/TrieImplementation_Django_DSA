from django.urls import path
from . import views

urlpatterns = [
    path('', views.trie, name='trie_view'),

    path('get_suggestions', views.get_suggestions, name='get_suggestions'),
    path('add_word', views.add_word, name='add_word'),
    path('view_words', views.view_words, name='view_words'),
    path('delete_words', views.delete_words, name='delete_words'),
    path('delete_word/<int:word_id>/', views.delete_word, name='delete_word'),
]