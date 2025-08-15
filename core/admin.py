from django.contrib import admin
from .models import Activity, Session, Announcement
from django.utils.html import format_html

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name","category", "image_thumb")
    readonly_fields = ("image_preview",)
    fields = ("name","slug","category","description","image","image_preview")
    inlines = [SessionInline]

    def image_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;">', obj.image.url)
        return "—"
    image_thumb.short_description = "Foto"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100%;height:auto;border-radius:8px;">', obj.image.url)
        return "Sin imagen"
    image_preview.short_description = "Vista previa"

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "is_pinned", "published_at")
    list_filter = ("is_pinned",)
    search_fields = ("title", "body")
    ordering = ("-is_pinned", "-published_at")
