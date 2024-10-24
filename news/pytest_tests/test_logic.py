from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

HOME_URL = reverse('news:home')


def test_anonymous_user_cant_create_comment(
        just_client,
        news,
        url_reverse
):
    just_client.post(*url_reverse)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
        author_client,
        form_data,
        news,
        author,
        url_reverse,
):
    author_client.post(*url_reverse)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(
        author_client,
        comment,
        news,
):
    news_url = reverse('news:detail',
                       args=(news.pk,))
    url_to_comments = news_url + '#comments'
    comments_count = Comment.objects.count()
    assert comments_count == 1
    response = author_client.delete(reverse(
        'news:delete', args=(comment.pk,))
    )
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
        author_client,
        comment,
        news,
        not_author_client
):
    response = not_author_client.delete(reverse(
        'news:delete', args=(comment.pk,))
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
        author_client,
        comment,
        news,
        form_data
):
    news_url = reverse('news:detail',
                       args=(news.pk,)) + '#comments'
    edit_url = reverse('news:edit',
                       args=(comment.pk,))
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, news_url)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(
        not_author_client,
        comment,
        news,
        form_data
):
    text_commet = comment.text
    edit_url = reverse('news:edit',
                       args=(comment.pk,))
    response = not_author_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == text_commet
