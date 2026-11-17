from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Category(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    TYPE_CHOICES = [(INCOME, "Income"), (EXPENSE, "Expense")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expense_categories")
    name = models.CharField(max_length=80)
    category_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    color = models.CharField(max_length=7, default="#6c63d9")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category_type", "name"]
        constraints = [
            models.UniqueConstraint(fields=["user", "name", "category_type"], name="unique_user_category_type")
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"


class Transaction(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    TYPE_CHOICES = [(INCOME, "Income"), (EXPENSE, "Expense")]
    PAYMENT_CHOICES = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("bank", "Bank transfer"),
        ("wallet", "Digital wallet"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    title = models.CharField(max_length=140)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    transaction_date = models.DateField(default=timezone.localdate)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="cash")
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-transaction_date", "-created_at"]
        indexes = [
            models.Index(fields=["user", "transaction_date"]),
            models.Index(fields=["user", "transaction_type"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.amount}"


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="budgets")
    month = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(2000)])
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "-month", "category__name"]
        constraints = [
            models.UniqueConstraint(fields=["user", "category", "month", "year"], name="unique_monthly_category_budget")
        ]

    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year}"
