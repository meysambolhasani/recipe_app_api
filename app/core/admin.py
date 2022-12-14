from django.contrib import admin
# import default user admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User,Tag,Ingredient,Recipe
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important Dates'), {'fields': ('last_login',)})

    )

    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2')
        }),
    )
# class UserAdminSite(admin.ModelAdmin):
#     list_display = ['email', 'name']
# admin.site.register(User, UserAdminSite)


admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
