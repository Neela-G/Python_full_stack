
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from decimal import Decimal, InvalidOperation
import secrets

from .forms import RegisterForm
from .models import BankAccount, Transaction


# Register View
def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            account_number = str(
                secrets.randbelow(9000000000) + 1000000000
            )

            while BankAccount.objects.filter(
                account_number=account_number
            ).exists():

                account_number = str(
                    secrets.randbelow(9000000000) + 1000000000
                )

            BankAccount.objects.create(
                user=user,
                account_number=account_number,
                balance=0
            )

            messages.success(request, 'Registration successful!')
            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


# Login View
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(
                request,
                'Invalid username or password'
            )

    return render(request, 'accounts/login.html')


# Logout View
@login_required
def logout_view(request):

    if request.method == 'POST':
        logout(request)
        return redirect('login')

    return redirect('dashboard')


# Dashboard View
@login_required
def dashboard_view(request):

    account = request.user.bankaccount

    return render(
        request,
        'accounts/dashboard.html',
        {'account': account}
    )


# Deposit View
@login_required
def deposit_view(request):

    if request.method == 'POST':

        try:
            amount = Decimal(request.POST.get('amount', ''))

            if not amount.is_finite() or amount <= 0:
                messages.error(
                    request,
                    'Enter a valid amount.'
                )

            else:
                account = request.user.bankaccount

                account.balance += amount
                account.save()

                Transaction.objects.create(
                    account=account,
                    transaction_type='Deposit',
                    amount=amount
                )

                messages.success(
                    request,
                    'Deposit successful!'
                )

        except (InvalidOperation, ValueError):
            messages.error(
                request,
                'Enter a valid amount.'
            )

    return redirect('dashboard')


# Withdraw View
@login_required
def withdraw_view(request):

    if request.method == 'POST':

        try:
            amount = Decimal(request.POST.get('amount', ''))

            if not amount.is_finite() or amount <= 0:
                messages.error(
                    request,
                    'Enter a valid amount.'
                )

            else:
                account = request.user.bankaccount

                if account.balance >= amount:

                    account.balance -= amount
                    account.save()

                    Transaction.objects.create(
                        account=account,
                        transaction_type='Withdraw',
                        amount=amount
                    )

                    messages.success(
                        request,
                        'Withdrawal successful!'
                    )

                else:
                    messages.error(
                        request,
                        'Insufficient balance!'
                    )

        except (InvalidOperation, ValueError):
            messages.error(
                request,
                'Enter a valid amount.'
            )

    return redirect('dashboard')
# Transaction History View
@login_required
def transaction_history_view(request):

    account = request.user.bankaccount

    transactions = Transaction.objects.filter(
        account=account
    ).order_by('-date')

    return render(
        request,
        'accounts/transactions.html',
        {'transactions': transactions}
    )