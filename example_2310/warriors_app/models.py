from django.contrib.auth.models import AbstractUser
from django.db import models


class Goods(models.Model):
    CATEGORY_CHOICES = (
        ('Vegetables', 'Vegetables'),
        ('Fruit', 'Fruit'),
        ('Meat', 'Meat'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    created = models.DateTimeField(verbose_name='Дата создания',
                                   auto_now_add=True, editable=True)
    price = models.IntegerField(verbose_name='Цена'
                                             '', default=0, blank=True, null=True)
    new_price = models.IntegerField(verbose_name='Новая цена', default=0, blank=True, null=True)

    def __str__(self):
        return self.name + ' / ' + str(self.created)


class FoodGoods(Goods):
    calory = models.CharField(max_length=100)


def get_upload_path(instance, filename):
    return "goods_image_{id}/{file}".format(id=instance.goods.id, file=filename)


class GoodsImage(models.Model):
    goods = models.ForeignKey(
        Goods,
        related_name='images',
        on_delete=models.CASCADE
    )
    image_key = models.CharField(max_length=10)
    file = models.FileField(upload_to=get_upload_path, null=True, blank=True, )

    def __str__(self):
        return str(self.file.name) + ' / ' + str(self.goods.id)


class User(AbstractUser):
    """
    Описание пользователя
    """
    tel = models.CharField("Телефон", max_length=15, blank=True, null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username


class Warrior(models.Model):
    """
    Описание война
    """

    race_types = (
        ('s', 'student'),
        ('d', 'developer'),
        ('t', 'teamlead'),
    )
    race = models.CharField(max_length=1, choices=race_types, verbose_name='Расса')
    name = models.CharField(max_length=120, verbose_name='Имя')
    level = models.IntegerField(verbose_name='Уровень', default=0)
    skill = models.ManyToManyField('Skill', verbose_name='Умения', through='SkillOfWarrior',
                                   related_name='warrior_skils', blank=True),
    profession = models.ForeignKey('Profession', on_delete=models.CASCADE, verbose_name='Профессия',
                                   blank=True, null=True)
    new_race = models.CharField(max_length=1, choices=race_types, verbose_name='Новая Расса', blank=True, null=True)
    new_race_2 = models.CharField(max_length=1, choices=race_types, verbose_name='Новая Расса 2', blank=True, null=True)

    def __str__(self):
        return self.name + ' / ' + str(self.id)

    def print_name(self):
        """
        Метод, выводящий имя
        """
        print(self.name)


class Profession(models.Model):
    """
    Описание профессии
    """

    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title + ' / ' + str(self.id)


class Skill(models.Model):
    """
    Описание умений
    """

    title = models.CharField(max_length=120, verbose_name='Наименование')

    def __str__(self):
        return self.title


class SkillOfWarrior(models.Model):
    """
    Описание умений война
    """

    skill = models.ForeignKey('Skill', verbose_name='Умение', on_delete=models.CASCADE)
    warrior = models.ForeignKey('Warrior', verbose_name='Воин', on_delete=models.CASCADE)
    level = models.IntegerField(verbose_name='Уровень освоения умения')


class Log(models.Model):
    """
    Лог
    """

    message = models.CharField(max_length=2048, verbose_name='Описание события')
    created = models.DateTimeField(verbose_name='Дата события',
                                   auto_now_add=True, editable=True)

    def __str__(self):
        return str(self.created)


