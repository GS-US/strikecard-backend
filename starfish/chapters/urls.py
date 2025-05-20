from django.urls import path
from .views import ChapterListView, ChapterDetailView

urlpatterns = [
    path('', ChapterListView.as_view(), name='chapter_list'),
    path('<int:pk>/', ChapterDetailView.as_view(), name='chapter_detail'),
]
