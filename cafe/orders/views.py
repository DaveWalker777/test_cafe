from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.db.models import Sum
from .forms import OrderForm, OrderStatusForm
from .models import Order
from .serializers import OrderSerializer
from rest_framework import viewsets


def order_list(request):
    """
    Отображение списка заказов с возможностью фильтрации по номеру стола и статусу.
    Фильтрация выполняется по переданному параметру 'search' в GET-запросе.

    :param request: HTTP запрос.
    :return: Рендеринг страницы с выводом списка заказов.
    """
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '')

    # Маппинг статусов на русском языке в английский
    status_mapping = {
        'В ожидании': 'pending',
        'Готово': 'ready',
        'Оплачено': 'paid',
    }

    # Если в запросе есть статус на русском, преобразуем его в английский
    if search_query in status_mapping:
        search_query = status_mapping[search_query]

    # Фильтруем заказы по номеру стола или статусу
    orders = Order.objects.filter(
        models.Q(table_number__icontains=search_query) |
        models.Q(status__icontains=search_query)
    )

    if status_filter:
        # Фильтруем по статусу
        orders = orders.filter(status=status_filter)

    # Обрабатываем и подсчитываем общую стоимость
    for order in orders:
        if order.items:
            order.items_list = [
                item.split(" ") for item in order.items.split("\n") if item
            ]
            order.total_price = sum(float(item[1]) for item in order.items_list)
        else:
            order.items_list = []
            order.total_price = 0.0

    return render(request, 'orders/order_list.html', {'orders': orders})


def revenue_for_shift(request):
    """
    Отображение выручки за смену, основанной на оплаченных заказах.
    Выручка рассчитывается по дате.

    :param request: HTTP запрос.
    :return: Рендеринг страницы с дневной выручкой.
    """
    # Фильтруем заказы с статусом 'оплачено' и группируем их по дате
    orders_paid = Order.objects.filter(status='paid')
    daily_revenue = orders_paid.values('created_at__date').annotate(total_revenue=Sum('total_price')).order_by('created_at__date')

    return render(request, 'orders/revenue.html', {'daily_revenue': daily_revenue})


def add_order(request):
    """
    Добавление нового заказа через форму. При успешной валидации заказа подсчитывается общая стоимость
    и заказ сохраняется в базе данных.

    :param request: HTTP запрос.
    :return: Перенаправление на список заказов после сохранения нового заказа.
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)  # Не сохраняем в базу данных сразу
            order.total_price = order.calculate_total_price()  # Подсчитываем общую стоимость
            order.save()  # Сохраняем заказ с подсчитанной стоимостью
            return redirect('order_list')  # Перенаправляем на страницу списка заказов
    else:
        form = OrderForm()

    return render(request, 'orders/add_order.html', {'form': form})


def update_order(request, order_id):
    """
    Обновление статуса заказа и его содержимого. Если заказ обновляется успешно,
    пользователю отображается сообщение об успехе.

    :param request: HTTP запрос.
    :param order_id: ID заказа для обновления.
    :return: Перенаправление на страницу списка заказов после успешного обновления.
    """
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        form = OrderStatusForm(request.POST)
        if form.is_valid():
            order.status = form.cleaned_data['status']

            # Проверяем, есть ли поле items в форме
            if 'items' in form.cleaned_data:
                order.items = form.cleaned_data['items']  # Обновляем содержимое заказа

            order.save()
            messages.success(request, "Заказ успешно обновлен")
            return redirect("order_list")
        else:
            messages.error(request, "Ошибка при обновлении заказа")
    else:
        # Передаем в форму текущее содержимое заказа
        form = OrderStatusForm(initial={"status": order.status, "items": order.items})

    return render(request, "orders/update_order.html", {"form": form, "order": order})


def delete_order(request, order_id):
    """
    Удаление заказа по его ID.

    :param request: HTTP запрос.
    :param order_id: ID заказа для удаления.
    :return: Перенаправление на страницу списка заказов после удаления.
    """
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с заказами через API.
    Поддерживает стандартные операции CRUD (создание, чтение, обновление, удаление).

    :param queryset: Запрос всех заказов.
    :param serializer_class: Сериализатор для модели Order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
