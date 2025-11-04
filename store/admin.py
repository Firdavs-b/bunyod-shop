from django.contrib import admin
from .models import Category, Product, Order,IncomingBatch, IncomingItem


class IncomingItemInline(admin.TabularInline):
    model = IncomingItem
    extra = 1
    fields = ('product', 'quantity', 'cost_price', 'total_cost', 'profit')
    readonly_fields = ('total_cost', 'profit')

    def total_cost(self, obj):
        return f"{obj.total_cost:.2f} сомонӣ"

    def profit(self, obj):
        return f"{obj.profit:.2f} сомонӣ"


@admin.register(IncomingBatch)
class IncomingBatchAdmin(admin.ModelAdmin):
    inlines = [IncomingItemInline]
    list_display = ('id', 'date_received', 'total_sum', 'total_profit')
    readonly_fields = ('total_sum', 'total_profit')

    def total_sum(self, obj):
        total = sum([item.total_cost for item in obj.items.all()])
        return f"{total:.2f} сомонӣ"
    total_sum.short_description = "Ҳамагӣ харид"

    def total_profit(self, obj):
        total = sum([item.profit for item in obj.items.all()])
        return f"{total:.2f} сомонӣ"
    total_profit.short_description = "Ҳамагӣ фоида"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','category','sell_price')
    list_filter = ('category',)
    search_fields = ('name','description')

# store/admin.py
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from .models import Order
from .forms import ProfitDateForm

# admin.py
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'phone', 'product', 'quantity',
        'payment_method', 'created_at', 'profit_amount', 'profit_percent'
    )
    list_filter = ('payment_method', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'address', 'product__name')

    # Фоидаи пулӣ
    def profit_amount(self, obj):
        if obj.product and obj.product.cost_price and obj.product.sell_price:
            return (obj.product.sell_price - obj.product.cost_price) * obj.quantity
        return 0
    profit_amount.short_description = 'Фоида (сом)'

    # Фоизи фоида
    def profit_percent(self, obj):
        if obj.product and obj.product.cost_price and obj.product.sell_price:
            return round(((obj.product.sell_price - obj.product.cost_price) / obj.product.cost_price) * 100, 2)
        return 0
    profit_percent.short_description = 'Фоизи фоида (%)'

    
from django.contrib import admin
from .models import DebtorClient, DebtorItem

class DebtorItemInline(admin.TabularInline):
    model = DebtorItem
    extra = 1
    fields = ('product', 'quantity', 'total_price', 'payment_status', 'debt_amount')
    readonly_fields = ('debt_amount',)

    def debt_amount(self, obj):
        # Агар obj.debt_amount None бошад, 0 истифода мешавад
        amount = obj.debt_amount or 0
        return f"{amount:.2f} сомонӣ"


@admin.register(DebtorClient)
class DebtorClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'total_debt', 'created_at')
    inlines = [DebtorItemInline]

    def total_debt(self, obj):
        total = sum([item.debt_amount or 0 for item in obj.items.all()])
        return f"{total:.2f} сомонӣ"
    total_debt.short_description = "Ҳамагӣ карз"
