import json

from rest_framework.views import APIView
from rest_framework.response import Response

from core.services import get_domain_list
from core.services import post_links


class VisitedLinks(APIView):
    """Вьюза принмает метод post и возращает json."""

    def post(self, request):
        """Принимает json с ключчем links и записывает в redis данные."""
        status = 'ok'
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            status = 'error'
        else:
            post_links(json_data.get('links', []))
        return Response(
            {
                'status': status,
            }
        )


class VisitedDomains(APIView):
    """Принимаает метод get и возвращает json."""

    def get(self, request):
        """Возвращает список уникальных доменов в формате json."""
        date_from = request.GET.get('from', '')
        date_to = request.GET.get('to', '')
        domain_list = get_domain_list(date_from, date_to)
        return Response(
            {
                'domains': domain_list,
                'status': 'ok',
            }
        )
