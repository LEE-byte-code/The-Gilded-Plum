from django.contrib import admin
from .models import MenuCategory, MenuItem, GalleryImage


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'order']
    list_filter = ['category', 'is_available', 'tags']
    search_fields = ['name', 'description', 'ingredients']
    list_editable = ['is_available', 'order', 'price']
    fieldsets = [
        ('Basic Info', {'fields': ['category', 'name', 'description', 'price', 'image', 'is_available', 'order']}),
        ('Ingredients & Nutrition', {'fields': ['ingredients', 'calories', 'protein', 'carbs', 'fat']}),
        ('Dietary', {'fields': ['allergens', 'tags']}),
        ('Story & Pairing', {'fields': ['chefs_note', 'wine_pairing']}),
    ]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['caption', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
