from django.contrib import admin
from .models import Article,Comment

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class ArticlenAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["Article_title",'Article_text']}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [CommentInline]
    # list_display = ["question_text", "pub_date", "was_published_recently"]
    # list_filter = ["pub_date"]
    # search_fields = ["question_text"]


admin.site.register(Article,ArticlenAdmin)