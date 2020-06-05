from typing import Tuple, Any

import pytest  # type: ignore

from datetime import datetime, timedelta

from main.db import RedisLinkStorage


LINKS_REQUEST_DATA = {"links": [
    "https://ya.ru",
    "https://ya.ru?q=123",
    "funbox.ru",
    "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
]}

LINKS_RESPONSE_DATA = {
    "status": "ok"
}

DOMAINS_RESPONSE_DATA = {
    "domains": {
        "ya.ru", "funbox.ru", "stackoverflow.com"
    },
    "status": "ok"
}


WRONG_LINKS_DATA: Tuple[str, Tuple] = (
    'data',
    (
        {"links": {}},
        {"links": [True]},
        {"links": [['rambler.ru']]},
        {},
    )
)


def mock_redis_client(redisdb, monkeypatch):
    def mock_result(cls):
        return redisdb

    monkeypatch.setattr(RedisLinkStorage, 'get_redis_client', mock_result)


@pytest.mark.urls('main.urls')
def test_endpoints(client, redisdb, monkeypatch):
    mock_redis_client(redisdb, monkeypatch)

    resp = client.post('/visited_links/', LINKS_REQUEST_DATA)
    assert resp.status_code == 200
    assert resp.data == LINKS_RESPONSE_DATA

    now = datetime.now()
    query_data = {
        "from": (now - timedelta(days=1)).timestamp(),
        "to": (now + timedelta(days=1)).timestamp(),
    }

    resp = client.get('/visited_domains/', query_data)
    assert resp.status_code == 200
    assert resp.data == DOMAINS_RESPONSE_DATA


@pytest.mark.parametrize(*WRONG_LINKS_DATA)
@pytest.mark.urls('main.urls')
def test_negative_links_endpoint(client, redisdb, monkeypatch, data):
    mock_redis_client(redisdb, monkeypatch)

    resp = client.post('/visited_links/', data)
    assert resp.status_code == 400
    assert isinstance(resp.data['status'], str)


@pytest.mark.urls('main.urls')
def test_negative_domains_endpoint(client, redisdb, monkeypatch):
    mock_redis_client(redisdb, monkeypatch)

    resp = client.get('/visited_domains/')
    assert resp.status_code == 400
    assert isinstance(resp.data['status'], str)
