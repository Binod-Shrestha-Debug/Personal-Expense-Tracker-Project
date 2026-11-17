import csv
from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import SignupForm, TransactionForm, CategoryForm, BudgetForm
from .models import Transaction, Category, Budget


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        # Give each new account a useful starting set of categories.
        defaults = [
            ("Salary", "income", "#22a06b"), ("Freelance", "income", "#3288d8"),
            ("Food", "expense", "#e69b42"), ("Transport", "expense", "#6c63d9"),
            ("Shopping", "expense", "#d96c9a"), ("Bills", "expense", "#5486b8"),
        ]
        Category.objects.bulk_create([
            Category(user=user, name=name, category_type=kind, color=color)
            for name, kind, color in defaults
        ])
        login(request, user)
        messages.success(request, "Welcome! Your account and starter categories are ready.")
        return redirect("dashboard")
    return render(request, "registration/signup.html", {"form": form})


def _month_bounds(year, month):
    start = date(year, month, 1)
    end = date(year + (month == 12), 1 if month == 12 else month + 1, 1)
    return start, end


@login_required
def dashboard(request):
    today = timezone.localdate()
    start, end = _month_bounds(today.year, today.month)
    month_qs = Transaction.objects.filter(user=request.user, transaction_date__gte=start, transaction_date__lt=end)
    income = month_qs.filter(transaction_type=Transaction.INCOME).aggregate(v=Sum("amount"))["v"] or Decimal("0")
    expenses = month_qs.filter(transaction_type=Transaction.EXPENSE).aggregate(v=Sum("amount"))["v"] or Decimal("0")
    recent = Transaction.objects.filter(user=request.user).select_related("category")[:7]

    labels, income_data, expense_data = [], [], []
    for offset in range(5, -1, -1):
        index = today.month - offset
        year = today.year
        while index <= 0:
            index += 12
            year -= 1
        month_start, month_end = _month_bounds(year, index)
        qs = Transaction.objects.filter(user=request.user, transaction_date__gte=month_start, transaction_date__lt=month_end)
        labels.append(month_start.strftime("%b %Y"))
        income_data.append(float(qs.filter(transaction_type="income").aggregate(v=Sum("amount"))["v"] or 0))
        expense_data.append(float(qs.filter(transaction_type="expense").aggregate(v=Sum("amount"))["v"] or 0))

    expense_categories = (
        month_qs.filter(transaction_type="expense", category__isnull=False)
        .values("category__name", "category__color")
        .annotate(total=Sum("amount")).order_by("-total")
    )
    context = {
        "income": income, "expenses": expenses, "balance": income - expenses,
        "recent_transactions": recent,
        "chart_labels": labels, "income_data": income_data, "expense_data": expense_data,
        "category_labels": [x["category__name"] for x in expense_categories],
        "category_values": [float(x["total"]) for x in expense_categories],
        "category_colors": [x["category__color"] for x in expense_categories],
        "month_name": today.strftime("%B %Y"),
    }
    return render(request, "tracker/dashboard.html", context)


def _filtered_transactions(request):
    qs = Transaction.objects.filter(user=request.user).select_related("category")
    query = request.GET.get("q", "").strip()
    kind = request.GET.get("type", "")
    category = request.GET.get("category", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(note__icontains=query) | Q(category__name__icontains=query))
    if kind in ("income", "expense"):
        qs = qs.filter(transaction_type=kind)
    if category.isdigit():
        qs = qs.filter(category_id=int(category))
    if start_date:
        try:
            qs = qs.filter(transaction_date__gte=date.fromisoformat(start_date))
        except ValueError:
            start_date = ""
    if end_date:
        try:
            qs = qs.filter(transaction_date__lte=date.fromisoformat(end_date))
        except ValueError:
            end_date = ""
    return qs, {"q": query, "type": kind, "category": category, "start_date": start_date, "end_date": end_date}


@login_required
def transaction_list(request):
    transactions, filters = _filtered_transactions(request)
    categories = Category.objects.filter(user=request.user)
    return render(request, "tracker/transaction_list.html", {
        "transactions": transactions, "categories": categories, "filters": filters,
    })


@login_required
def transaction_create(request):
    form = TransactionForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        messages.success(request, "Transaction added successfully.")
        return redirect("transaction_list")
    return render(request, "tracker/transaction_form.html", {"form": form, "page_title": "Add transaction"})


@login_required
def transaction_update(request, pk):
    item = get_object_or_404(Transaction, pk=pk, user=request.user)
    form = TransactionForm(request.POST or None, instance=item, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Transaction updated successfully.")
        return redirect("transaction_list")
    return render(request, "tracker/transaction_form.html", {"form": form, "page_title": "Edit transaction"})


@login_required
def transaction_delete(request, pk):
    item = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Transaction deleted.")
        return redirect("transaction_list")
    return render(request, "tracker/confirm_delete.html", {"item": item, "kind": "transaction"})


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, "tracker/category_list.html", {"categories": categories})


@login_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        try:
            category.save()
            messages.success(request, "Category created.")
            return redirect("category_list")
        except Exception:
            form.add_error(None, "A category with this name and type already exists.")
    return render(request, "tracker/category_form.html", {"form": form})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted. Existing transactions will remain uncategorized.")
    return redirect("category_list")


@login_required
def budget_list(request):
    today = timezone.localdate()
    budgets = Budget.objects.filter(user=request.user).select_related("category")
    rows = []
    for budget in budgets:
        start, end = _month_bounds(budget.year, budget.month)
        spent = Transaction.objects.filter(
            user=request.user, category=budget.category, transaction_type="expense",
            transaction_date__gte=start, transaction_date__lt=end
        ).aggregate(v=Sum("amount"))["v"] or Decimal("0")
        percent = min(float(spent / budget.amount * 100), 100) if budget.amount else 0
        rows.append({"budget": budget, "spent": spent, "percent": percent, "over": spent > budget.amount})
    return render(request, "tracker/budget_list.html", {"budget_rows": rows, "today": today})


@login_required
def budget_create(request):
    form = BudgetForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        budget = form.save(commit=False)
        budget.user = request.user
        try:
            budget.save()
            messages.success(request, "Monthly budget saved.")
            return redirect("budget_list")
        except Exception:
            form.add_error(None, "A budget already exists for this category and month.")
    return render(request, "tracker/budget_form.html", {"form": form})


@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == "POST":
        budget.delete()
        messages.success(request, "Budget deleted.")
    return redirect("budget_list")


@login_required
def reports(request):
    transactions, filters = _filtered_transactions(request)
    income = transactions.filter(transaction_type="income").aggregate(v=Sum("amount"))["v"] or Decimal("0")
    expenses = transactions.filter(transaction_type="expense").aggregate(v=Sum("amount"))["v"] or Decimal("0")
    by_category = (
        transactions.filter(transaction_type="expense", category__isnull=False)
        .values("category__name").annotate(total=Sum("amount")).order_by("-total")
    )
    return render(request, "tracker/reports.html", {
        "income": income, "expenses": expenses, "net": income - expenses,
        "by_category": by_category, "filters": filters,
    })


@login_required
def export_transactions(request):
    transactions, filters = _filtered_transactions(request)
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="expense-tracker-transactions.csv"'
    response.write("\ufeff")
    writer = csv.writer(response)
    writer.writerow(["Date", "Title", "Type", "Category", "Amount", "Payment method", "Note"])
    for item in transactions:
        writer.writerow([
            item.transaction_date, item.title, item.get_transaction_type_display(),
            item.category.name if item.category else "", item.amount,
            item.get_payment_method_display(), item.note,
        ])
    return response
