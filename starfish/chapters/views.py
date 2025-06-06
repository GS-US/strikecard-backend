from django.views.generic import DetailView, ListView

from .models import Chapter


class ChapterListView(ListView):
    model = Chapter
    template_name = 'chapters/chapter_list.html'


class ChapterDetailView(DetailView):
    model = Chapter
    template_name = 'chapters/chapter_detail.html'
