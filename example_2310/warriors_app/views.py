from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django_filters import rest_framework as filters
from rest_framework import filters as standart_filters
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AddWarrior
from .serializers import *


@require_http_methods(["GET"])
def get_warrior_data(request, id):
    warrior = get_object_or_404(Warrior, id=id)
    return render(request, 'warrior.html', {'warrior': warrior})


@require_http_methods(["GET", "POST"])
def add_warrior(request):
    form = AddWarrior(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f'/warrior/{form.instance.id}/')

    return render(request, 'add_warrior.html', {'form': form})


class GoodsListViewWithApiView(APIView):
    # Переписываем метод get

    def get(self, request):
        goods = Goods.objects.all()[:10]
        goods_list = GoodsSerializer(goods, many=True)
        return Response(goods_list.data)

    def post(self, request):
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Goods
        fields = ['category', 'min_price', 'max_price']


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 3
#     page_size_query_param = 'page_size' # GoodsListView/?p=2&page_size=3
#     page_query_param = 'page' # GoodsListView/?p=2
#     max_page_size = 100


class CustomPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'  # GoodsListView/?p=2&page_size=3
    page_query_param = 'p'  # GoodsListView/?p=2
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'message': 'it`s ok',
            'count': self.page.paginator.count,
            'results': data
        })


class GoodsListGenericView(generics.ListCreateAPIView):
    """
         Список продуктов
    """
    queryset = Goods.objects.all()
    # Сериализация
    serializer_class = GoodsSerializer

    # # Пагинация
    # pagination_class = CustomPagination

    # Фильтр / сортировка, поиск
    #filter_backends = [standart_filters.SearchFilter, standart_filters.OrderingFilter, filters.DjangoFilterBackend]
    #ordering_fields = ['created']
    # search_fields = ['name', 'category']
    filterset_class = ProductFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print('ddddddddddd')
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GoodsCreateGenericView(generics.CreateAPIView):
    """
         Список продуктов
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer


class GoodsImageCreateGenericView(generics.CreateAPIView):
    """
    Сериалайзер для загрузки изображений товаров
    """
    queryset = Goods.objects.all()
    serializer_class = GoodImagesManyCreateSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     instance_serializer = GoodsSerializer(Goods.objects.get(id=request.data['goods']))
    #     return Response(instance_serializer.data)

    def post(self, request):
        serializer = GoodImagesManyCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            new_serializer = GoodsSerializer(Goods.objects.get(id=request.data['goods']))
            return Response(new_serializer.data)
        return Response({'success': "False"}, status=status.HTTP_400_BAD_REQUEST)


class GoodsOneImageCreateGenericView(generics.CreateAPIView):
    """
    Сериалайзер для загрузки изображений товаров
    """
    queryset = GoodsImage.objects.all()
    serializer_class = GoodImagesSerializer


class GoodsListViewSetView(viewsets.ModelViewSet):
    """
         Список продуктов
    """
    queryset = Goods.objects.all()
    # Сериализация
    serializer_class = GoodsSerializer
    # Пагинация
    # pagination_class = StandardResultsSetPagination
    # Фильтр / сортировка, поиск
    #  = [standart_filters.SearchFilter, standart_filters.OrderingFilter, filters.DjangoFilterBackend]
    # ordering_fields = ['created']
    # search_fields = ['name', 'category']
    filterset_class = ProductFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        print('ddddd')
        return Response(serializer.data)


class SkillAPIView(APIView):

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})


class SkillCreateView(APIView):
    '''
    Example:
        {
            "skill": {"title": "dddd"}
        }
    '''

    def post(self, request):
        global skill_saved
        skill = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({"Success": "Skill '{}' created".format(skill_saved.title)})


class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class ProfessionCreateView(APIView):

    def post(self, request):
        print("REQUEST DATA", request.data)
        profession = request.data.get("profession")
        print("PROF DATA", profession)

        serializer = ProfessionCreateSerializer(data=profession)

        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()

        return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})


class WarriorListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class WarriorListRelatedAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorRelatedSerializer


class WarriorListDepthAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorDepthSerializer


class WarriorListNestedAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorNestedSerializer

    def post(self, request):
        serializer = WarriorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorSerializer(warrior, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        try:
            warrior.delete()
            return Response(status=200)
        except:
            return Response(status=400)


class WarriorCreateAPIView(generics.ListCreateAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


class WarriorDestroyView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class WarriorUpdateView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class WarriorDetailsView(generics.RetrieveAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class ProfessionCreateAPIView(generics.CreateAPIView):
    serializer_class = ProfessionCreateSerializer
    queryset = Profession.objects.all()


# @transaction.atomic
# @api_view(['POST'])
# def create_prof_and_connect_to_warrior(request):
#     """
#     Эндпоинт на создания профессии и привязки его к воину
#     принимает следюущий словарь на вход:
#     {
#     "prof_name":"имя профессии",
#     "prof_description":"Описание профессии",
#     "warrior_id":2
#     }
#     """
#     data = request.data
#     # Создание новой профессии
#     new_prof = Profession.objects.create(title=data["prof_name"],
#                                          description=data["prof_description"])
#     # Создание война
#     warrior = Warrior.objects.get(id=data["warrior_id"])
#
#     # Привязка профессии к воину
#     warrior.profession = new_prof
#     warrior.save()
#
#     return Response(status=201, data={"message": "objects created"})


@api_view(['POST'])
def create_prof_and_connect_to_warrior(request):
    """
    Эндпоинт на создания профессии и привязки его к воину
    принимает следюущий словарь на вход:
    {
    "prof_name":"имя профессии",
    "prof_description":"Описание профессии",
    "warrior_id":2
    }
    """
    data = request.data
    # Поиск война
    warrior = Warrior.objects.filter(id=data["warrior_id"])
    if warrior.exists():
        # Создание новой профессии
        new_prof = Profession.objects.create(title=data["prof_name"], description=data["prof_description"])
        warrior[0].profession = new_prof
        warrior[0].save()
        return Response(status=201, data={"message": "objects created"})
    return Response(status=404, data={"message": "Warrior not found"})


@api_view(['GET', 'POST'])
def warrior_list(request):
    if request.method == 'POST':
        serializer = WarriorSerializer(data=request.data)
        if serializer.is_valid():
            # Если полученные данные валидны — выполняем работу
            # Например, сохраняем данные в базу через save() (как при работе с формами)
            serializer.save()
            # Возвращаем JSON с полученными данными и статус-код 200
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Если данные не прошли валидацию — возвращаем сообщение об ошибке:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
