from django.views.generic import DetailView

from .models import Chapter


class ChapterDetailView(DetailView):
    model = Chapter
    template_name = 'chapters/chapter_detail.html'
