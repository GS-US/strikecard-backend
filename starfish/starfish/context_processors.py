from .utils import get_totals


def the_totals(request):
    return {'the_totals': get_the_totals()}
