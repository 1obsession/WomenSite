from django.contrib import admin, messages
from django.db.models import Q
from django.db.models.functions import Length
from django.utils.safestring import mark_safe

from .models import Women, Category


class ContentFilter(admin.SimpleListFilter):
    title = "Сортировка по статьям"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('short', "Короткие статьи"),
            ('middle', "Средние статьи"),
            ('long', "Большие статьи"),
        ]

    def queryset(self, request, queryset):
        queryset = queryset.annotate(length=Length('content'))
        if self.value() == 'short':
            return queryset.filter(length__lt=1000)
        elif self.value() == 'middle':
            return queryset.filter(length__gte=1000, length__lt=5000)
        elif self.value() == 'long':
            return queryset.filter(length__gte=5000)

class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'husband', 'tag']
    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug': ['title']}
    filter_horizontal = ['tag']
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat',)
    list_display_links = ('title', )
    ordering = ['time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter, ContentFilter, 'cat__name', 'is_published']
    save_on_top = True

    @admin.display(description='Изображение', ordering=Length('content'))
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50")
        else:
            return "Нет Фото"

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {count} записей')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} записей', messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
