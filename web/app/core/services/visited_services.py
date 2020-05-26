import datetime
import re
from typing import List
from typing import Set
import redis

from django.conf import settings



domain_regex = (r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+'
                r'[a-z0-9][a-z0-9-]{0,61}[a-z0-9]')


def init_redis() -> redis.Redis:
    """Возвращает конект к redis"""
    redis_instance = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0
    )
    return redis_instance


def get_domain_list(date_from: int, date_to: int) -> Set[str]:
    """Выберает уникальные доменны в пределенном диапазоне."""
    redis_instance = init_redis()
    domain_set = set()
    # если дата form больше даты to то меняем ихместами.
    if date_from > date_to:
        date_from, date_to = date_to, date_from
    url_list = redis_instance.zrangebyscore('urls', date_from, date_to)
    # выбераем только уникальные домены.
    for url in url_list:
        search = re.search(domain_regex, url.decode('utf-8'))
        if search:
            domain_set.add(search.group(0))
    return domain_set


def post_links(links: List[str]) -> None:
    """Добавляет данные в redis в упорядоченное множество."""
    redis_instance = init_redis()
    timestamp = int(datetime.datetime.now().timestamp())
    for link in links:
        redis_instance.zadd('urls', {link: timestamp})
