from rest_framework import serializers  # type: ignore

from main.utils import validate_url


class UrlField(serializers.CharField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(validate_url)


class LinksSerializer(serializers.Serializer):
    links = serializers.ListField(child=UrlField())

    def __init__(self, visit_timestamp, link_storage, *args, **kwargs):
        self.visit_timestamp = visit_timestamp
        self.link_storage = link_storage
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        return self.link_storage.add_links(
            validated_data['links'],
            self.visit_timestamp,
        )
