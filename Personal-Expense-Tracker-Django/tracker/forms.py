from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction, Category, Budget


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["title", "transaction_type", "category", "amount", "transaction_date", "payment_method", "note"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Grocery shopping"}),
            "amount": forms.NumberInput(attrs={"min": "0.01", "step": "0.01", "placeholder": "0.00"}),
            "transaction_date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 4, "placeholder": "Optional details..."}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(user=user)
        self.fields["category"].required = False
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-select" if name in ("category", "transaction_type", "payment_method") else "form-control"

    def clean(self):
        cleaned = super().clean()
        category = cleaned.get("category")
        transaction_type = cleaned.get("transaction_type")
        if category and transaction_type and category.category_type != transaction_type:
            self.add_error("category", "Choose a category matching the transaction type.")
        return cleaned


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "category_type", "color"]
        widgets = {"name": forms.TextInput(attrs={"placeholder": "e.g. Food"}),
                   "color": forms.TextInput(attrs={"type": "color"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-select" if name == "category_type" else "form-control"


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["category", "month", "year", "amount"]
        widgets = {
            "month": forms.Select(choices=[(i, name) for i, name in enumerate(
                ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]) if i]),
            "year": forms.NumberInput(attrs={"min": "2000", "max": "2100"}),
            "amount": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(user=user, category_type=Category.EXPENSE)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-select" if name in ("category", "month") else "form-control"
