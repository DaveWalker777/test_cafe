import pytest
from .models import Order


@pytest.mark.django_db
def test_calculate_total_price():
    # Тестируем заказ с двумя блюдами
    order = Order.objects.create(
        table_number=1,
        items="Вода 100\nПепси 200",
        total_price=0.0,
        status=Order.PENDING
    )
    # Проверяем, что стоимость расчитывается корректно
    assert order.calculate_total_price() == 300.0


@pytest.mark.django_db
def test_calculate_total_price_invalid_data():
    # Тестируем заказ с некорректной ценой
    order = Order.objects.create(
        table_number=1,
        items="Вода 100\nПепси abc",  # Некорректная цена
        total_price=0.0,
        status=Order.PENDING
    )
    # Проверяем, что некорректные данные игнорируются
    assert order.calculate_total_price() == 100.0


@pytest.mark.django_db
def test_order_creation():
    # Тестируем создание заказа
    order = Order.objects.create(
        table_number=1,
        items="Вода 100\nПепси 200",
        total_price=0.0,
        status=Order.PENDING
    )
    assert order.table_number == 1
    assert order.calculate_total_price() == 300.0
    assert order.status == Order.PENDING
