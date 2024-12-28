from django.contrib import admin
from .models import Bankist
# Register your models here.


class BankistAdminDisplay(admin.ModelAdmin):
  list_display = ('account_number', 'user_profile__user__username', 'balance')
  search_fields = ('account_number', 'user__username')
  list_filter = ('user_profile__user__username',)
  
admin.site.register(Bankist,BankistAdminDisplay)