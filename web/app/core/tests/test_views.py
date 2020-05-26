import json
import pytest

from django.urls import reverse_lazy

from core.services import init_redis


def test_debug():
    assert 1 == 1


@pytest.mark.parametrize(
    'parameters',
    (
        # url name, status,
        ('visited_domains', 200),
        ('visited_links', 405),

    )
)
class TestGetView:
    """Проверяем все ливьюхи возвращают нужные статусы."""
    def test_factory_views(self, parameters, client):
        """ """
        url_name, code = parameters
        url = reverse_lazy(url_name)
        response = client.get(url)
        assert response.status_code == code


@pytest.mark.parametrize(
    'parameters',
    (
        # url_name, status
        ('visited_links', 200),
        ('visited_domains', 405)
    )
)
class TestPosTView:
    """Тест на пост запросы. """

    def test_factory_views(self, parameters, client):
        """Проверка вьюх на метод post."""
        url_name, code = parameters
        url = reverse_lazy(url_name)
        response = client.post(url)
        assert response.status_code == code


@pytest.fixture
def create_redis(request):
    """Фикстура создает истенс redis"""
    redis_client = init_redis()
    request.addfinalizer(redis_client.flushall)
    return redis_client


@pytest.fixture
def create_links(create_redis):
    """Фикстура создает даные для базы Redis."""
    urls = [
        'https://ya.ru',
        'https://ya.ru?q=123',
        'funbox.ru',
        'https://stackoverflow.com/questions/11828270'
    ]
    time_create = 1545221231
    for url in urls:
        create_redis.zadd('urls', {url: time_create})


def test_get_visited_domains_view(create_links, client):
    """Тестим получение данных в заданном диапазоне."""
    date_from = '1545221231'
    date_to = '1545217638'
    url = reverse_lazy('visited_domains')
    url_with_parameters = f'{url}?from={date_from}&to={date_to}'
    response = client.get(url_with_parameters)
    json_data = json.loads(response.content)
    assert response.status_code == 200
    assert json_data['status'] == 'ok'
    for domain in json_data['domains']:
        assert domain in ['ya.ru', 'stackoverflow.com', 'funbox.ru']


def test_create_visited_links(client):
    """Тест проверки view создание списка ссылок."""
    url = reverse_lazy('visited_links')
    data = {
        'links': [
            'https://ya.ru',
            'https://ya.ru?q=123',
            'funbox.ru',
            'https://stackoverflow.com/questions/11828270/'
        ]
    }
    response = client.post(url, data=data, content_type='application/json')
    json_data = json.loads(response.content)
    assert json_data['status'] == 'ok'


# перенести в другой файлик.
def test_resis_connect():
    """Тест подключения к базе Redis"""
    connect = init_redis()
    assert connect.ping()

