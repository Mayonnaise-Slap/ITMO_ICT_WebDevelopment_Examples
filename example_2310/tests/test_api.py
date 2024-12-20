from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from warriors_app.models import Warrior
from collections import OrderedDict


class WarriorsTests(APITestCase):

    @classmethod
    def setUpTestData(self): # Метод для создания тестовых данных
        Warrior.objects.create(race = 's', name = 'Bob', level = 5) # Создание тестового экземпляра
        # война. Объет создается в песочнице и не влияет на основую базу данных


    # def test_get_warrior(self):
    #     url = reverse('warriors_app:warriors')
    #     # указание на url-адрес, который подвергается тестированию
    #     data = {"id": 1, "race": "s", "name": "Bob"}
    #     # набор данных с которыми будет производиться сравнение полученных от бэкенда данных
    #     response = self.client.get(url, data, format='json')
    #     # получение (GET) данных (data) по указанному url-адресу (url) в формате json (format)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     # сравнение статус полученного ответа и стандартного статус кода успешного получения данных
    #     # Справочно: 200 OK — успешный запрос от клиента серверу.
    #     self.assertEqual(response.json().get('Warriors'), [data])
    #     # Cравнение данных полученных из ответа сервера (response.json().get('Warriors')) с тестовыми данными (data)


    def test_create_warrior(self):
        url = reverse('warriors_app:warrior_create')
        # указание на url-адрес, который подвергается тестированию
        data = {"id": 2, "race": "s", "name": "Bob"}
        # набор данных для отправки в POST запросе
        response = self.client.post(url, data, format='json')
        # отправка (POST) данных (data) по указанному url-адресу (url) в формате json (format)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # сравнение статус полученного ответа и стандартного статус кода успешного получения данных
        # Справочно: 201 OK — успешный POST запрос от клиента серверу.
        self.assertEqual(response.data, data)
        # Cравнение данных полученных из ответа сервера (response.json().get('Warriors')) с данными, который были отосланы на сервер в POST запросе (data)