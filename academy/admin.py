from django.contrib import admin
from .models import Booklet, ContactMessage, Post, PostCategory, TeacherProfile


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "telegram_username", "email", "updated_at")


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "is_featured", "created_at")
    list_filter = ("is_published", "is_featured", "category")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published", "is_featured")


@admin.register(Booklet)
class BookletAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "item_type",
        "level",
        "price_toman",
        "discount_price_toman",
        "is_available",
        "is_featured",
    )
    list_filter = ("item_type", "level", "is_available", "is_featured")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_available", "is_featured")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "subject", "telegram_or_phone", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("full_name", "subject", "message", "telegram_or_phone", "email")
    list_editable = ("is_read",)
    readonly_fields = ("created_at",)
