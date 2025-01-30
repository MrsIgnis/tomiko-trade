from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from .models import Cars, Brands
from .forms import FeedbackForm
from parsers.models import VKClip, Review2GIS
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def main(request):
    clips = VKClip.objects.all()[:11]
    reviews = Review2GIS.objects.all()[:8]

    context = {
        'clips': clips,
        'reviews': reviews
    }

    return render(request, 'main_page.html', context)

def actions(request):
    return render(request, 'stocks.html')

def contacts(request):
    form = FeedbackForm()
    context = {'form': form}

    return render(request, 'contacts.html', context)

def work_cond(request):
    return render(request, 'work_cond.html')


def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)

def card(request):
    return render(request, 'card.html')

def get_sort_order(sort_option):
    """ Возвращает список полей для сортировки на основе параметра sort_option. """

    sort_dict = {
        'price_asc': 'price',
        'price_desc': '-price',
        'year_asc': 'year',
        'year_desc': '-year',
        'mileage_asc': 'mileage',
        'mileage_desc': '-mileage',
        'volume_asc': 'engine_volume',
        'volume_desc': '-engine_volume',
    }
    return sort_dict.get(sort_option, 'None')

def get_colors_list():
    """Возвращает список цветов с их отображаемыми именами."""

    colors_list = ['Красный', 'Синий', 'Зеленый','Белый','Розовый',
                   'Серебряный', 'Серый', 'Бежевый', 'Бордовый', 'Желтый',
                   'Золотой', 'Оранжевый', 'Коричневый', 'Фиолетовый',]

    return colors_list

def get_mileage_values():
    """ Создает список возможных вариантов пробега с шагом в 10.000 """

    min_mileage = Cars.objects.all().order_by('mileage').first()
    max_mileage = Cars.objects.all().order_by('-mileage').first()

    if min_mileage and max_mileage:
        min_val = min_mileage.mileage // 10000 * 10000
        max_val = max_mileage.mileage // 10000 * 10000 + 10000
    else:
        return []

    return list(range(min_val, max_val, 10000))

def get_country_dict():
    """Возвращает словарь стран."""
    country_dict = {
        'japan': 'Япония',
        'korea': 'Корея',
        'china': 'Китай',
    }

    return country_dict

def get_models_by_brand(request, country):
    brand_name = request.GET.get('brand')
    country = get_country_dict().get(country)

    if brand_name and country:
        try:
            brand = Brands.objects.get(brand=brand_name, country__iexact=country)
            models = Cars.objects.filter(brand_country=brand).values_list('model', flat=True).distinct().order_by('model')
            return JsonResponse(list(models), safe=False)

        except Brands.DoesNotExist:
            return JsonResponse([], safe=False)

    else:
        return JsonResponse([], safe=False)

def cars_catalog(request, country):
    """ Отображает список автомобилей с сортировкой и пагинации. """

    # Параметры фильтрации
    brand = request.GET.get('brand')
    model = request.GET.get('model')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    volume_from = request.GET.get('volume_from')
    volume_to = request.GET.get('volume_to')
    drive = request.GET.get('drive')
    mileage_from = request.GET.get('mileage_from')
    mileage_to = request.GET.get('mileage_to')
    transmission = request.GET.get('transmission')
    color = request.GET.get('color')

    # Применение фильтрации
    filters = {}
    if brand: filters['brand_country__brand'] = brand
    if model: filters['model'] = model
    if year_from: filters['year__gte'] = year_from
    if year_to: filters['year__lte'] = year_to
    if volume_from: filters['engine_volume__gte'] = volume_from
    if volume_to: filters['engine_volume__lte'] = volume_to
    if drive: filters['drive'] = drive
    if mileage_from: filters['mileage__gte'] = mileage_from
    if mileage_to: filters['mileage__lte'] = mileage_to
    if transmission: filters['transmission'] = transmission
    if color: filters['color'] = color
    if country: filters['brand_country__country__iexact'] = get_country_dict().get(country)

    # Параметры сортировки
    sort_option = request.GET.get('sort', 'None')
    sort_fields = get_sort_order(sort_option)

    # Базовый запрос
    cars = Cars.objects.select_related('brand_country')

    # Фильтрация на основе собранных параметров
    cars = cars.filter(**filters)

    # Полное название авто
    cars = cars.annotate(full_name=Concat('brand_country__brand', Value(' '), 'model', output_field=CharField()))

    # Применение сортировки
    if sort_fields == "None": cars = cars.order_by('full_name')
    else: cars = cars.order_by(sort_fields)

    # Получаем 5 случайных автомобилей для текущей страны
    popular_cars = Cars.objects.filter(brand_country__country=get_country_dict().get(country)).order_by('?')[:5]

    # Пагинация
    paginator = Paginator(cars, 12)
    page = request.GET.get('page')

    try:
        cars_page = paginator.get_page(page)
    except PageNotAnInteger:
        cars_page = paginator.page(1)

    # Получаем уникальные данные для фильтра
    available_brands = Brands.objects.filter(country=get_country_dict().get(country)).values_list('brand', flat=True).distinct().order_by('brand')
    available_years = Cars.objects.values_list('year', flat=True).distinct().order_by('year')
    available_volumes = Cars.objects.values_list('engine_volume', flat=True).distinct().order_by('engine_volume')
    available_drives = Cars.objects.values_list('drive', flat=True).distinct().order_by('drive')
    available_mileages = get_mileage_values()
    available_transmissions = Cars.objects.values_list('transmission', flat=True).distinct().order_by('transmission')
    available_colors = get_colors_list()

    available_models = []
    if brand: available_models = cars.values_list('model', flat=True).distinct().order_by('model')

    context = {
        'cars_page': cars_page,
        'sort_option': sort_option,
        'available_brands': available_brands,
        'available_models': available_models,
        'available_years': available_years,
        'available_volumes': available_volumes,
        'available_drives': available_drives,
        'available_mileages': available_mileages,
        'available_transmissions': available_transmissions,
        'available_colors': available_colors,
        'current_country': country,
        'popular_cars': popular_cars,
    }

    return render(request, 'catalogs.html', context)

@require_POST
def submit_feedback(request):
    form = FeedbackForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)