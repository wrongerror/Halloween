from django.contrib import admin

# Register your models here.
from django.contrib import admin
import models

class ProductionImageInline(admin.TabularInline):
    model = models.ProductionImage

class ProductionAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    inlines = [ProductionImageInline]
    search_fields = ['name',]

admin.site.register(models.Production, ProductionAdmin)
admin.site.register(models.Designer)
admin.site.register(models.Vote)