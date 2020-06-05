
При разработке использовался `python 3.8`. Зависимости находятся в `requirements.txt`

Подготовка к запуску:
```
virtualenv -p python3.8 .venv
source ./.venv/bin/activate
pip install -r ./requirements.txt
```

Запустить сервер:
`python ./manage.py runserver 8000`

Запустить тесты:
`pytest ./tests/test_endpoints.py`

Автоматически сгенерированное API можно посмотреть по адресу:
`http://localhost:8000/`
