from django.contrib import admin
from .models import Post, Subscription


admin.site.register(Post)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)


