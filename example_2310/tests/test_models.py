from django.test import TestCase

# Create your tests here.

from warriors_app.models import Warrior

class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):  # Метод для создания тестовых данных
        # Set up non-modified objects used by all test methods
        Warrior.objects.create(race = 's', name = 'Bob', level = 5)
        # Создание тестового экземпляра война. Объект создается в песочнице и не влияет на основную базу данных


    def test_race_label(self):
        author=Warrior.objects.get(race = 's', name = 'Bob', level = 5) # Получение объекта из бд
        field_label = author._meta.get_field('race').verbose_name # Получение свойства объекта, значение
        # которого будет проверяться в тесте
        self.assertEquals(field_label,'Расса')
        # сравнение полученного из БД значени я поля и указанного в теста (расса)

    def test_name_label(self):
        author=Warrior.objects.get(race = 's', name = 'Bob', level = 5)
        field_label = author._meta.get_field('name').verbose_name
        self.assertEquals(field_label,'Имя')

    def test_race_max_length(self):
        author=Warrior.objects.get(race = 's', name = 'Bob', level = 5)
        max_length = author._meta.get_field('race').max_length
        self.assertEquals(max_length,1)

    def test_object_name_is_name(self):
        author=Warrior.objects.get(race = 's', name = 'Bob', level = 5)
        expected_object_name = '%s' % author.name
        self.assertEquals(expected_object_name,str(author))

