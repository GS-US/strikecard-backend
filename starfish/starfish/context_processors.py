from .utils import get_totals

def totals(request):
    return {'totals': get_totals()}
