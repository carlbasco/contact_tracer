from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from .forms import *
from .models import*

@admin.register(Province)
class ProvinceAdmin(ImportExportModelAdmin):
    list_display=('id','name')
    list_per_page=100

@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    exclude = ('id', )
    search_fields =('name',)
    list_per_page=20

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ('email','full_name')
    list_filter = ('groups',)
    fieldsets = (
        (None, 
        {'fields': ('email', 'password','first_name','middle_name','last_name','suffix')}),
        ('Role', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','first_name','middle_name','last_name','suffix', 'groups')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)