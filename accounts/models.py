
from django.db import models
from django.contrib.auth.models import User


# Bank Account Model
class BankAccount(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    account_number = models.CharField(
        max_length=16,
        unique=True
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return self.account_number


# Transaction Model
class Transaction(models.Model):

    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
    ]

    account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
