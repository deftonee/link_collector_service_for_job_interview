import redis

from abc import ABC, abstractmethod
from typing import List

from django.conf import settings  # type: ignore


class LinkStorage(ABC):

    @abstractmethod
    def add_link(self, link: str, timestamp: float) -> None:
        pass

    @abstractmethod
    def get_links(
            self,
            from_timestamp: float,
            to_timestamp: float
    ) -> List[str]:
        pass

    def add_links(self, links: List[str], timestamp: float) -> int:
        for link in links:
            self.add_link(link, timestamp)
        return len(links)


class RedisLinkStorage(LinkStorage):

    def __init__(self):
        self.client = self.get_redis_client()

    @classmethod
    def get_redis_client(cls):
        return redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
        )

    def add_link(self, link: str, timestamp: float) -> None:
        n = self.client.hlen(settings.LINKS_STORAGE_KEY)
        self.client.hset(
            settings.LINKS_STORAGE_KEY,
            n,
            link,
        )
        self.client.zadd(
            settings.TIMESTAMPS_STORAGE_KEY,
            {n: timestamp},
        )

    def get_links(
            self,
            from_timestamp: float,
            to_timestamp: float
    ) -> List[str]:
        link_keys = self.client.zrangebyscore(
            settings.TIMESTAMPS_STORAGE_KEY,
            from_timestamp,
            to_timestamp,
        )
        links = []
        for link_key in link_keys:
            links.append(
                self.client.hget(
                    settings.LINKS_STORAGE_KEY, link_key,
                ).decode()
            )
        return links
