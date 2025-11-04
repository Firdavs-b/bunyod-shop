from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=120, verbose_name="Номи категория")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Сурат (категория)")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категорияҳо"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=200, verbose_name="Номи маҳсулот")
    description = models.TextField(blank=True, null=True, verbose_name="Тавсиф")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Нархи харид")
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Нархи фурӯш")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Сурат")

    class Meta:
        verbose_name = "Маҳсулот"
        verbose_name_plural = "Маҳсулотҳо"

    def __str__(self):
        return self.name


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Нақд'),
        ('card', 'Корти бонкӣ'),
        ('transfer', 'Пулгузаронӣ (QR/аппа)'),
    ]

    first_name = models.CharField(max_length=80, verbose_name="Ном")
    last_name = models.CharField(max_length=80, verbose_name="Насаб")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    address = models.CharField(max_length=250, verbose_name="Суроға")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Маҳсулот")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Миқдор")
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='cash', verbose_name="Тарзи пардохт")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Санаи фармоиш")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказҳо"

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.product.name}"




class IncomingBatch(models.Model):
    date_received = models.DateField(auto_now_add=True, verbose_name="Санаи воридот")
    note = models.CharField(max_length=255, blank=True, null=True, verbose_name="Шарҳ")

    class Meta:
        verbose_name = "Воридоти нав"
        verbose_name_plural = "Воридотҳои нав"

    def __str__(self):
        return f"Воридот {self.date_received}"

class IncomingItem(models.Model):
    batch = models.ForeignKey(IncomingBatch, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Маҳсулот")
    quantity = models.PositiveIntegerField(verbose_name="Миқдор", null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Нархи харид (як дона)", null=True, blank=True)

    @property
    def total_cost(self):
        if self.quantity is not None and self.cost_price is not None:
            return self.quantity * self.cost_price
        return 0

    @property
    def profit(self):
        if self.quantity is not None and self.cost_price is not None and self.product.sell_price is not None:
            return (self.product.sell_price - self.cost_price) * self.quantity
        return 0

from django.db import models
from .models import Product

class DebtorClient(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Номи аввал")
    last_name = models.CharField(max_length=100, verbose_name="Номи охир")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(blank=True, null=True, verbose_name="Суроға")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Санаи фармоиш")

    class Meta:
        verbose_name = "Клиент карздор"
        verbose_name_plural = "Клиентҳои карздор"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DebtorItem(models.Model):
    client = models.ForeignKey(DebtorClient, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Маҳсулот")
    quantity = models.PositiveIntegerField(verbose_name="Миқдор")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Маблағи умумӣ")
    payment_status = models.BooleanField(default=False, verbose_name="Пардохт шуд/нашуд")

    @property
    def debt_amount(self):
        if not self.payment_status:
            return self.total_price
        return 0

    def __str__(self):
        return f"{self.product.name} — {self.quantity} дона"

    class Meta:
        verbose_name = "Маҳсулоти карздор"
        verbose_name_plural = "Маҳсулотҳои карздор"
    