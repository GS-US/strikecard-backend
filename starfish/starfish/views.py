from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import get_the_totals


class GetTotalsView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response(get_the_totals())
