from django.urls import path

from .views import ChapterDetailView, ChapterListView

urlpatterns = [
    path('', ChapterListView.as_view(), name='chapter_list'),
    path('<str:slug>/', ChapterDetailView.as_view(), name='chapter_detail'),
]
