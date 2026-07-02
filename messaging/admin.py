from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'content', 'created_at')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('listing', 'buyer', 'seller', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'content_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)

    def _is_allowed_admin(self, request):
        """Allow deletion for users with accounts.profile.role == 'admin'.

        Fallback: if profile/role is missing or misconfigured, allow staff/superusers too,
        so admin deletion works reliably."""
        if not request or not request.user.is_authenticated:
            return False

        if getattr(request.user, 'is_superuser', False):
            return True
        if getattr(request.user, 'is_staff', False):
            return True

        profile = getattr(request.user, 'profile', None)
        return bool(profile and getattr(profile, 'role', None) == 'admin')


    def has_delete_permission(self, request, obj=None):
        return self._is_allowed_admin(request)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self._is_allowed_admin(request):
            return qs
        return qs.none()

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Content'


