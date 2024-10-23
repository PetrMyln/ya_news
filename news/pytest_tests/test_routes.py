import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from http import HTTPStatus


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, news_obj',
    (
            ('news:home', None),
            ('news:detail', pytest.lazy_fixture('pk_for_args_news')),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
    )
)
def test_pages_availability(client, name, news_obj, news):
    url = reverse(name, args=news_obj)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


#@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
            (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_availability_for_comment_edit_and_delete(
        parametrized_client,
        expected_status,
        name,
        pk_for_args_comment
):
    url = reverse(name, args=pk_for_args_comment)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status

@pytest.mark.parametrize(
    'name, comment_object',
    (
            ('news:edit', pytest.lazy_fixture('comment')),
            ('news:delete', pytest.lazy_fixture('comment')),
    ),
)

def test_redirect_for_anonymous_client(
        client, name,
        comment_object,
        pk_for_args_comment
):
    login_url = reverse('users:login')
    url = reverse(name, args=pk_for_args_comment)
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
