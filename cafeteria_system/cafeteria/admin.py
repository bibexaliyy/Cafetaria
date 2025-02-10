from django.contrib import admin
from django.urls import reverse
from .models import Student,Meal ,MealTransaction,MealTicket
from django.utils.html import format_html
admin.site.register(Meal)
admin.site.register(Student)
admin.site.register(MealTransaction)
admin.site.register(MealTicket)

class MealTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'meal', 'date', 'validity_days', 'download_ticket')

    def download_ticket(self, obj):
        return format_html('<a href="{}" target="_blank">Download PDF</a>',
                           reverse('generate_meal_ticket', args=[obj.id]))

    download_ticket.short_description = "Print Ticket"


