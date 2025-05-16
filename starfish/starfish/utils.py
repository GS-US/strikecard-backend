from django.db.models import Sum

from chapters.models import PaperTotal
from contacts.models import Contact, ExpungedContact
from partners.models import Pledge


def get_totals():
    active = Contact.objects.count()
    expunged = ExpungedContact.objects.count()
    pledged = Pledge.objects.aggregate(Sum('count'))['count__sum']
    paper = PaperTotal.objects.aggregate(Sum('count'))['count__sum']

    return {
        'active': active,
        'expunged': expunged,
        'pledged': pledged,
        'paper': paper,
        'total': active + expunged + pledged + paper,
    }
