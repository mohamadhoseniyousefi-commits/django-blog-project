from django.contrib import admin
from . import  models



class FilterByTitle(admin.SimpleListFilter):
    title = 'کلمه های پر تکرار'
    parameter_name = 'title'


    def lookups(self, request, model_admin):
        return (
        ("tehran","تهران"),
        ("rasht","رشت"),
        )


    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(title__icontains=self.value())


class CommentInline(admin.StackedInline):
    model = models.Comment



@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display =("title","author","status","get_image")
    list_filter = ("status",FilterByTitle)
    search_fields = ("title","body")
    inlines = (CommentInline,)




admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Messages)
admin.site.register(models.Likes)