import pytest
from django.conf import settings
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture

HOME_URL = reverse('news:home')


@pytest.mark.django_db
def test_news_count(client, many_news):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, many_news):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(
        client,
        create_comments_for_news,
        news,
        create_detail_url):
    url = create_detail_url
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert sorted_timestamps == all_timestamps


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, form_status',
    (
            (lazy_fixture('just_client'), False),
            (lazy_fixture('author_client'), True),
    ),
)
def test_form_exist_for_different_users(
        create_detail_url,
        parametrized_client,
        form_status):
    url = create_detail_url
    response = parametrized_client.get(url)
    assert ('form' in response.context) is form_status
