from django.db import models


class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Menu categories'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.CharField(max_length=500, blank=True, help_text='Path or URL to dish image')
    is_available = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    ingredients = models.TextField(blank=True)
    calories = models.PositiveIntegerField(default=0)
    protein = models.CharField(max_length=20, blank=True)
    carbs = models.CharField(max_length=20, blank=True)
    fat = models.CharField(max_length=20, blank=True)
    allergens = models.CharField(max_length=500, blank=True, help_text='Comma-separated list')
    chefs_note = models.TextField(blank=True)
    wine_pairing = models.CharField(max_length=300, blank=True)
    tags = models.CharField(max_length=300, blank=True, help_text='Comma-separated list (e.g. vegetarian, gluten-free)')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__order', 'order']

    def __str__(self):
        return f"{self.name} — ${self.price}"

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def allergen_list(self):
        return [a.strip() for a in self.allergens.split(',') if a.strip()]


class GalleryImage(models.Model):
    image = models.CharField(max_length=500)
    caption = models.CharField(max_length=300)
    alt_text = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Gallery image'
        verbose_name_plural = 'Gallery images'

    def __str__(self):
        return self.caption
