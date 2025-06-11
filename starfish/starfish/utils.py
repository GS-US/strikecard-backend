from chapters.models import OfflineTotal
from contacts.models import Contact, ExpungedContact
from django.conf import settings
from django.db.models import Sum
from partners.models import Pledge


def get_the_totals():
    active = Contact.objects.count()
    expunged = ExpungedContact.objects.count()
    pledged = Pledge.objects.aggregate(Sum('count'))['count__sum'] or 0
    offline = OfflineTotal.objects.aggregate(Sum('count'))['count__sum'] or 0
    total = active + expunged + pledged + offline

    return {
        'active': active,
        'expunged': expunged,
        'pledged': pledged,
        'offline': offline,
        'total': total,
        'needed': settings.FINAL_COUNT - total,
    }
