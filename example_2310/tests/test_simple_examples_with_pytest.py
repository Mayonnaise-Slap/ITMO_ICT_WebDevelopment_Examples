import pytest
from warriors_app.models import Warrior, Profession, Skill, SkillOfWarrior

@pytest.fixture
def profession():
    """
    Фикстура для создания объекта Profession.
    """
    return Profession.objects.create(title="Мечник", description="Воин, владеющий мечом")

@pytest.fixture
def skill():
    """
    Фикстура для создания объекта Skill.
    """
    return Skill.objects.create(title="Владение мечом")

@pytest.fixture
def warrior(profession):
    """
    Фикстура для создания объекта Warrior.
    """
    return Warrior.objects.create(race="h", name="Ланселот", level=5, profession=profession)

@pytest.fixture
def skill_of_warrior(skill, warrior):
    """
    Фикстура для создания объекта SkillOfWarrior.
    """
    return SkillOfWarrior.objects.create(skill=skill, warrior=warrior, level=3)


@pytest.mark.django_db
def test_warrior_creation(warrior):
    """
    Проверяем, что объект Warrior успешно создается.
    """
    assert isinstance(warrior, Warrior)
    assert warrior.name == "Ланселот"


@pytest.mark.django_db
def test_profession_creation(profession):
    """
    Проверяем, что объект Profession успешно создается.
    """
    assert isinstance(profession, Profession)
    assert profession.title == "Мечник"


@pytest.mark.django_db
def test_skill_creation(skill):
    """
    Проверяем, что объект Skill успешно создается.
    """
    assert isinstance(skill, Skill)
    assert skill.title == "Владение мечом"


@pytest.mark.django_db
def test_skill_of_warrior_creation(skill_of_warrior):
    """
    Проверяем, что объект SkillOfWarrior успешно создается.
    """
    assert isinstance(skill_of_warrior, SkillOfWarrior)
    assert skill_of_warrior.warrior.name == "Ланселот"
    assert skill_of_warrior.skill.title == "Владение мечом"
    assert skill_of_warrior.level == 3


@pytest.mark.django_db
def test_profession_in_warrior(warrior):
    """
    Проверяем, что у воина есть связанная профессия.
    """
    assert warrior.profession.title == "Мечник"


@pytest.mark.django_db
def test_warrior_skill_relationship(warrior, skill_of_warrior):
    """
    Проверяем связь между воином и умениями через SkillOfWarrior.
    """
    skills = SkillOfWarrior.objects.filter(warrior=warrior)
    assert skills.count() == 1
    assert skills.first().skill.title == "Владение мечом"


@pytest.mark.django_db
def test_increase_skill_level(skill_of_warrior):
    """
    Проверяем логику увеличения уровня умения.
    """
    skill_of_warrior.level += 1
    skill_of_warrior.save()
    assert skill_of_warrior.level == 4


@pytest.mark.django_db
def test_delete_warrior_cascades_skillofwarrior(warrior, skill_of_warrior):
    """
    Проверяем, что при удалении воина связанные записи SkillOfWarrior удаляются.
    """
    warrior.delete()
    assert SkillOfWarrior.objects.filter(warrior=warrior).count() == 0
