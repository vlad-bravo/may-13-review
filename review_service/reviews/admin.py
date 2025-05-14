from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'rating')
    search_fields = ('user', )
    list_filter = ('user', )
    empty_value_display = '-пусто-'
