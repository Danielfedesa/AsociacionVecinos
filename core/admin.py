from django.contrib import admin
from .models import Activity, Session, Announcement

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "location")
    list_filter = ("category",)
    search_fields = ("name", "description", "location")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SessionInline]

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "is_pinned", "published_at")
    list_filter = ("is_pinned",)
    search_fields = ("title", "body")
    ordering = ("-is_pinned", "-published_at")
