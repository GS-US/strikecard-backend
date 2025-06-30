from chapters.models import OfflineTotal
from django.conf import settings
from django.contrib.humanize.templatetags import humanize
from django.db.models import Sum
from members.models import ExpungedMember, Member
from partners.models import Pledge


def get_the_totals():
    active = Member.objects.count()
    expunged = ExpungedMember.objects.count()
    pledged = Pledge.objects.aggregate(Sum('count'))['count__sum'] or 0
    offline = OfflineTotal.objects.aggregate(Sum('count'))['count__sum'] or 0
    total = active + expunged + pledged + offline

    totals = {
        'active': active,
        'expunged': expunged,
        'pledged': pledged,
        'offline': offline,
        'total': total,
        'final': settings.FINAL_COUNT,
        'needed': settings.FINAL_COUNT - total,
    }

    return dict(
        totals, **{f'{k}_str': humanize.intcomma(str(v)) for k, v in totals.items()}
    )
