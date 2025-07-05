from django.contrib import admin
from .models import MenuItem, MenuCategory, MenuItemCategory, ALLERGEN_CHOICES

class MenuItemCategoryInline(admin.TabularInline):
    model = MenuItemCategory
    extra = 1

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_vegan', 'contains_pork', 'allergens_display', 'is_available')
    list_filter = ('is_vegan', 'contains_pork', 'is_available')
    search_fields = ('name', 'description')
    inlines = [MenuItemCategoryInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'description', 'image')
        }),
        ('食事制限情報', {
            'fields': ('allergens', 'is_vegan', 'contains_pork')
        }),
        ('管理情報', {
            'fields': ('is_available',)
        }),
    )
    
    def allergens_display(self, obj):
        """アレルギー物質を表示用に整形"""
        allergen_dict = dict(ALLERGEN_CHOICES)
        allergens = [allergen_dict.get(a, a) for a in obj.allergens]
        return ', '.join(allergens) if allergens else 'なし'
    
    allergens_display.short_description = 'アレルギー物質'

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'display_order')
    search_fields = ('name', 'description')
    ordering = ('display_order', 'name')
    inlines = [MenuItemCategoryInline]
