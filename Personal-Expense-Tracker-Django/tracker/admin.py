from django.contrib import admin
from .models import Category, Transaction, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category_type", "user", "created_at")
    list_filter = ("category_type",)
    search_fields = ("name", "user__username")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "transaction_type", "amount", "transaction_date", "category", "user")
    list_filter = ("transaction_type", "payment_method", "transaction_date")
    search_fields = ("title", "note", "user__username")
    date_hierarchy = "transaction_date"


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("category", "month", "year", "amount", "user")
    list_filter = ("month", "year")
