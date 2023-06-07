import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pjt.settings")
django.setup()

import csv
from recipes.models import *
from accounts.models import User

with open('recipe_data/닭볶음탕진짜진짜.csv', 'r', encoding='utf-8') as file:
    csv_data = csv.reader(file)
    next(csv_data)
    for row in csv_data:
        print(row[4])
        # recipe = Recipe()
        # recipe.title = row[0]
        # recipe.user = User.objects.get(pk='1')
        # recipe.content = row[2]
        # recipe.category = row[3]
        # recipe.image = row[4]
        # recipe.time = row[5]
        # recipe.difficulty = row[6]

        # recipe.save()

        # i = 7
        # while 1:
        #     # print(row[i])
        #     # seq_recipe_ingredient = f'recipe_ingredient_{i}'
        #     seq_recipe_ingredient = RecipeIngredient()
            
        #     if row[i] == '끝':
        #         break
            
        #     ingre, qtt = row[i].split(',')
        #     my_ingre = Ingredient.objects.get_or_create(name=ingre)
            
        #     seq_recipe_ingredient.recipe = recipe
        #     seq_recipe_ingredient.ingredient = my_ingre[0]
        #     seq_recipe_ingredient.quantity = qtt
        #     seq_recipe_ingredient.save()
        #     i += 1
        # i += 1
        # while 1:
        #     # seq_recipe_step = f'recipe_step_{i}'
        #     seq_recipe_step = RecipeStep()
        #     if row[i] == '끝':
        #         break
        #     print(recipe, row[i])
        #     seq_recipe_step.recipe = recipe
        #     seq_recipe_step.detail = row[i]
        #     i += 1
        #     seq_recipe_step.save()