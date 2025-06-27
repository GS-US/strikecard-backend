from .utils import get_the_totals


def the_totals(request):
    return {'the_totals': get_the_totals()}


def hide_save_and_add_another(request):
    return {'show_save_and_add_another': False}
