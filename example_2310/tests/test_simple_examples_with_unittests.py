from django.test import TestCase
from warriors_app.models import Warrior, Profession, Skill, SkillOfWarrior


class WarriorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Подготавливаем тестовые данные, которые будут использоваться во всех тестах.
        """
        # Создаем профессию
        cls.profession = Profession.objects.create(
            title="Мечник", description="Воин, владеющий мечом"
        )

        # Создаем умение
        cls.skill = Skill.objects.create(title="Владение мечом")

        # Создаем воина
        cls.warrior = Warrior.objects.create(
            race="h", name="Ланселот", level=5, profession=cls.profession
        )

        # Добавляем умение воину
        cls.skill_of_warrior = SkillOfWarrior.objects.create(
            skill=cls.skill, warrior=cls.warrior, level=3
        )

    def test_warrior_creation(self):
        """
        Проверяем, что объект Warrior успешно создается.
        """
        self.assertTrue(isinstance(self.warrior, Warrior))
        self.assertEquals(self.warrior.name, "Ланселот")

    def test_profession_creation(self):
        """
        Проверяем, что объект Profession успешно создается.
        """
        self.assertTrue(isinstance(self.profession, Profession))
        self.assertEquals(self.profession.title, "Мечник")

    def test_skill_creation(self):
        """
        Проверяем, что объект Skill успешно создается.
        """
        self.assertTrue(isinstance(self.skill, Skill))
        self.assertEquals(self.skill.title, "Владение мечом")

    def test_skill_of_warrior_creation(self):
        """
        Проверяем, что объект SkillOfWarrior успешно создается и связан с воином и умением.
        """
        self.assertTrue(isinstance(self.skill_of_warrior, SkillOfWarrior))
        self.assertEquals(self.skill_of_warrior.warrior.name, "Ланселот")
        self.assertEquals(self.skill_of_warrior.skill.title, "Владение мечом")
        self.assertEquals(self.skill_of_warrior.level, 3)

    def test_profession_in_warrior(self):
        """
        Проверяем, что у воина есть связанная профессия.
        """
        self.assertEquals(self.warrior.profession.title, "Мечник")

    def test_warrior_skill_relationship(self):
        """
        Проверяем связь умения с воином через SkillOfWarrior.
        """
        skills = SkillOfWarrior.objects.filter(warrior=self.warrior)
        self.assertEquals(skills.count(), 1)
        self.assertEquals(skills.first().skill.title, "Владение мечом")

    def test_increase_skill_level(self):
        """
        Проверяем логику увеличения уровня умения в модели SkillOfWarrior.
        """
        self.skill_of_warrior.level += 1
        self.skill_of_warrior.save()
        self.assertEquals(self.skill_of_warrior.level, 4)

    def test_delete_warrior_cascades_skillofwarrior(self):
        """
        Проверяем, что при удалении воина связанные записи SkillOfWarrior удаляются.
        """
        self.warrior.delete()
        skills = SkillOfWarrior.objects.filter(warrior=self.warrior)
        self.assertEquals(skills.count(), 0)