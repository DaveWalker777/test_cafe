from django.db import models


class Order(models.Model):
    # Статусы заказа с соответствующими значениями и метками на русском языке
    PENDING = 'pending'
    READY = 'ready'
    PAID = 'paid'

    STATUS_CHOICES = [
        (PENDING, 'В ожидании'),
        (READY, 'Готово'),
        (PAID, 'Оплачено'),
    ]

    table_number = models.IntegerField()
    items = models.TextField()  # Храним строку с блюдами
    total_price = models.FloatField(default=0.0)  # Храним общую стоимость
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ {self.id}"

    def calculate_total_price(self):
        """
        Метод для подсчета общей стоимости блюд из строки.
        """
        total = 0
        if self.items:
            items_list = self.items.split("\n")
            for item in items_list:
                parts = item.split()
                if len(parts) == 2:
                    try:
                        total += float(parts[1])  # Суммируем стоимость блюд
                    except ValueError:
                        continue  # Игнорируем некорректные строки
        return total
