import sys
import traceback

import ipdb
from django.core.exceptions import PermissionDenied
from django.core.handlers.exception import response_for_exception
from django.utils.deprecation import MiddlewareMixin


class IPDBExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        exc_type, exc_value, tb = sys.exc_info()
        if exc_type == PermissionDenied:
            return
        traceback.print_exception(exc_type, exc_value, tb)
        ipdb.post_mortem(tb)
        return response_for_exception(request, exc_type, exc_value, tb)
