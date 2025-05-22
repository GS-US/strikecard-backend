from django.conf import settings
from django.db.models import Sum

from chapters.models import PaperTotal
from contacts.models import Contact, ExpungedContact
from partners.models import Pledge


def get_totals():
    active = Contact.objects.count()
    expunged = ExpungedContact.objects.count()
    pledged = Pledge.objects.aggregate(Sum('count'))['count__sum'] or 0
    paper = PaperTotal.objects.aggregate(Sum('count'))['count__sum'] or 0
    total = active + expunged + pledged + paper

    return {
        'active': active,
        'expunged': expunged,
        'pledged': pledged,
        'paper': paper,
        'total': total,
        'needed': settings.FINAL_COUNT - total,
    }
