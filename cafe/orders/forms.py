from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Форма для добавления/редактирования заказа.
    Включает в себя поля: номер стола и список блюд.
    Проверяет правильность ввода списка блюд с ценами.
    """

    class Meta:
        model = Order
        fields = ['table_number', 'items']

    def clean_items(self):
        """
        Чистит и валидирует поле 'items'. Преобразует строку блюд в формат, где каждая строка содержит
        название блюда и цену. Если формат неверный, возбуждается исключение.

        :return: Строка с правильным форматом (название блюда и цена через пробел).
        :raises: forms.ValidationError: Если формат блюда или цена неверны.
        """
        items = self.cleaned_data['items']

        # Разбиваем строку по новой строке и пробелам
        items_list = items.replace("\n", " ").split()

        # Проверка корректности формата (название и цена через пробел)
        items_parsed = []
        for i in range(0, len(items_list), 2):  # Шаг 2: название, цена
            item_name = items_list[i]
            try:
                item_price = float(items_list[i + 1])  # Преобразуем цену в число

                # Проверка, что цена не отрицательная
                if item_price < 0:
                    raise forms.ValidationError(f"Цена блюда '{item_name}' не может быть отрицательной.")

                items_parsed.append(f"{item_name} {item_price}")
            except IndexError:
                raise forms.ValidationError(f"Некорректный формат: отсутствует цена для блюда '{item_name}'.")
            except ValueError:
                raise forms.ValidationError(f"Некорректная цена для блюда '{item_name}': должно быть число.")

        # Возвращаем строку, соединяя все блюда с их ценами
        return "\n".join(items_parsed)

    def clean_table_number(self):
        table_number = self.cleaned_data.get('table_number')
        if table_number <= 0 or table_number > 50:
            raise forms.ValidationError("Номер стола должен быть положительным числом в диапазоне от 1 до 50.")
        return table_number


class OrderStatusForm(forms.ModelForm):
    """
    Форма для редактирования статуса заказа и его содержимого (блюда).
    Включает поля: статус и список блюд.
    """

    class Meta:
        model = Order
        fields = ['status', 'items']  # Позволяет изменять только статус и список блюд

    def clean_items(self):
        """
        Чистит и валидирует поле 'items'. Преобразует строку блюд в формат, где каждая строка содержит
        название блюда и цену. Если формат неверный или цена отрицательная, возбуждается исключение.

        :return: Строка с правильным форматом (название блюда и цена через пробел).
        :raises: forms.ValidationError: Если формат блюда или цена неверны.
        """
        items = self.cleaned_data['items']

        # Разбиваем строку по новой строке и пробелам
        items_list = items.replace("\n", " ").split()

        # Проверка корректности формата (название и цена через пробел)
        items_parsed = []
        for i in range(0, len(items_list), 2):  # Шаг 2: название, цена
            item_name = items_list[i]
            try:
                item_price = float(items_list[i + 1])  # Преобразуем цену в число

                # Проверка, что цена не отрицательная
                if item_price < 0:
                    raise forms.ValidationError(f"Цена блюда '{item_name}' не может быть отрицательной.")

                items_parsed.append(f"{item_name} {item_price}")
            except IndexError:
                raise forms.ValidationError(f"Некорректный формат: отсутствует цена для блюда '{item_name}'.")
            except ValueError:
                raise forms.ValidationError(f"Некорректная цена для блюда '{item_name}': должно быть число.")

        # Возвращаем строку, соединяя все блюда с их ценами
        return "\n".join(items_parsed)

    def clean_table_number(self):
        """
        Проверяет, что номер стола находится в диапазоне от 1 до 50.
        """
        table_number = self.cleaned_data.get('table_number')
        if table_number <= 0 or table_number > 50:
            raise forms.ValidationError("Номер стола должен быть положительным числом в диапазоне от 1 до 50.")
        return table_number
