
from django.contrib import admin
from .models import TravelPackage, Car, Addon, Customer
from django.contrib.auth.admin import UserAdmin

class CustomerAdmin(UserAdmin):
    model = Customer
    list_display = ('username', 'email', 'customer_number', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('customer_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('customer_number',)}),
    )
admin.site.register(Customer, CustomerAdmin)
admin.site.register(TravelPackage)
admin.site.register(Car)
admin.site.register(Addon)
