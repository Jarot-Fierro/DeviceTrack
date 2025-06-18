from django.contrib import admin

from .models import Transaction, TransactionOutput, SupportTransaction, DetailTransaction

admin.site.register(Transaction)
admin.site.register(TransactionOutput)
admin.site.register(SupportTransaction)
admin.site.register(DetailTransaction)
