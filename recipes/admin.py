from django.contrib import admin
from .models import *


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, RecipeStepInline)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)