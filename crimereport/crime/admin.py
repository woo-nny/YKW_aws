from django.contrib import admin
from .models import Congressperson, Saying # Region

# Register your models here.
@admin.register(Congressperson)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'district', 'crimes', 'penalty', 'photo', 'elected_num','party']


@admin.register(Saying)
class UserAdmin(admin.ModelAdmin):
    list_display = ['speaker', 'saying']
