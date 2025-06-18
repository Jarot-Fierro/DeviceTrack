from django.contrib import admin

from .models import Printer, PrinterHistory

admin.site.register(Printer)
admin.site.register(PrinterHistory)
