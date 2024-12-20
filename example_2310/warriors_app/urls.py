from django.conf.urls import url, include
from django.urls import path
from django.urls import register_converter
from rest_framework.routers import DefaultRouter

from .views import *


class ZipCodeConverter:
    # Регулярное выражение для проверки формата почтового кода (ZIP кода).
    regex = r'\d{5}'

    def to_python(self, value):
        try:
            # Преобразует значение в целое число (int).
            return int(value)
        except ValueError:
            # Если значение не может быть преобразовано в int, выбрасываем 404 ошибку.
            raise Http404("Неверный формат почтового кода")

    def to_url(self, value):
        # Преобразует значение обратно в строку (как обычно пятизначное число).
        return str(value)


# Регистрируем свой конвертер с именем 'zipcode'.
register_converter(ZipCodeConverter, 'zipcode')

app_name = "warriors_app"

router = DefaultRouter()
router.register(r'goods_with_viewset',
                GoodsListViewSetView, basename='good_view_set')

urlpatterns = [
    path('warrior/<int:id>/', get_warrior_data, name='warrior_detail'),  # Страница с деталями о воине
    path('warrior/add/', add_warrior, name='add_warrior'),  # Добавление нового воина

    path('goods_list_with_apiview/', GoodsListViewWithApiView.as_view()),
    path('goods_list_with_generic/', GoodsListGenericView.as_view()),
    path('goods_create_with_generic/', GoodsCreateGenericView.as_view()),
    # path('goods_list_with_viewset/', GoodsListViewSetView.as_view()),
    url(r'^', include(router.urls)),
    path('goods_image_many_create/', GoodsImageCreateGenericView.as_view()),
    path('goods_image_create/', GoodsOneImageCreateGenericView.as_view()),

    path('skills/', SkillAPIView.as_view()),
    path('skills/create/', SkillCreateView.as_view()),
    path('warriors/', WarriorAPIView.as_view()),
    path('warrior/create', WarriorCreateAPIView.as_view(), name='warrior_create'),
    path('warrior/detail/<int:pk>', WarriorDetailsView.as_view()),
    path('warrior/delete/<int:pk>', WarriorDestroyView.as_view()),
    path('warrior/update/<int:pk>', WarriorUpdateView.as_view()),

    path('warriors1/', WarriorAPIView.as_view(), name='warriors'),
    path('warriors/list/', WarriorListAPIView.as_view()),
    path('warriors/list/related/', WarriorListRelatedAPIView.as_view()),
    path('warriors/list/depth/', WarriorListDepthAPIView.as_view()),
    path('warriors/list/nested/', WarriorListNestedAPIView.as_view()),

    path('profession/create/', ProfessionCreateView.as_view()),
    path('profession/generic_create/', ProfessionCreateAPIView.as_view()),
    path('warrior/create1', WarriorCreateAPIView.as_view()),
    path('warrior/detail/<int:pk>', WarriorDetailsView.as_view()),
    path('warrior/delete/<int:pk>', WarriorDestroyView.as_view()),
    path('warrior/update/<int:pk>', WarriorUpdateView.as_view()),

    path('profession/create_with_warrior', create_prof_and_connect_to_warrior),

    path('location/<zipcode:postal_code>/', WarriorDetailsView.as_view()),

]
