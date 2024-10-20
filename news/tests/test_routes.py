# news/tests/test_routes.py
# Импортируем класс HTTPStatus.
from http import HTTPStatus

from django.test import TestCase
# Импортируем функцию reverse().
from django.urls import reverse
# Импортируем класс модели новостей.
from news.models import News

class TestRoutes(TestCase):


    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(title='Заголовок', text='Текст')
    def test_home_page(self):
        # Вместо прямого указания адреса
        # получаем его при помощи функции reverse().
        url = reverse('news:home')
        response = self.client.get(url)
        # Проверяем, что код ответа равен статусу OK (он же 200).
        self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_detail_page(self):
        # or url = reverse('news:detail', args=(self.news.pk,))
        # url = reverse('news:detail', args=(self.news.id,))
        # url = reverse('news:detail', kwargs={'pk': self.news.id})

        url = reverse('news:detail', kwargs={'pk': self.news.pk})
        response = self.client.get(url)
        #print(response.status_code)
        #print(response.templates)
        self.assertEqual(response.status_code, HTTPStatus.OK)
