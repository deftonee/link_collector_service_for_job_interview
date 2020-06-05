import tldextract  # type: ignore

from typing import Set, List

from django.core.exceptions import ValidationError  # type: ignore


def link_list_to_domain_set(link_list: List) -> Set:
    domains = map(
        lambda x: tldextract.extract(x).registered_domain,
        link_list,
    )
    return set(domains)


def validate_url(url: str) -> None:
    try:
        result = tldextract.extract(url).registered_domain
        if not result:
            raise ValueError
    except (TypeError, ValueError):
        raise ValidationError('Invalid URL')
