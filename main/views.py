from datetime import datetime

from rest_framework import status  # type: ignore
from rest_framework.exceptions import ValidationError  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore

from main.db import RedisLinkStorage
from main.serializers import LinksSerializer
from main.utils import link_list_to_domain_set


class VisitedLinksAPIView(APIView):

    def post(self, request):
        link_storage = RedisLinkStorage()

        serializer = LinksSerializer(
            visit_timestamp=datetime.now().timestamp(),
            link_storage=link_storage,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


class VisitedDomainsAPIView(APIView):

    def get(self, request):
        try:
            from_timestamp = float(request.GET.get('from'))
            to_timestamp = float(request.GET.get('to'))
        except (ValueError, TypeError):
            raise ValidationError(
                'Query parameters `from` and `to` containing '
                'timestamps should be set'
            )

        link_storage = RedisLinkStorage()
        links = link_storage.get_links(from_timestamp, to_timestamp)

        domains = link_list_to_domain_set(links)
        return Response(
            {'domains': domains},
            status=status.HTTP_200_OK,
        )
