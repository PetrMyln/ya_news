import pytest
from django.test.client import Client
from django.conf import settings
from datetime import datetime, timedelta

from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def just_client(author):
    client = Client()
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def many_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def pk_for_args_news(news):
    return (news.pk,)


@pytest.fixture
def pk_for_args_comment(comment):
    return (comment.pk,)


@pytest.fixture
def create_comments_for_news(news, author):
    now = timezone.now()
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE):
        # Создаём объект и записываем его в переменную.
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        # Сразу после создания меняем время создания комментария.
        comment.created = now + timedelta(days=index)
        # И сохраняем эти изменения.
        comment.save()


@pytest.fixture
def create_detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def form_data():
    return {
        'text': 'Коммент',
    }


@pytest.fixture()
def url_reverse(news, form_data):
    return reverse('news:detail', args=(news.id,), ), form_data
