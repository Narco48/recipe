from django.contrib import admin
from .models import *


admin.site.register(Categories)
admin.site.register(Recipe)
admin.site.register(FavouriteRecipe)
admin.site.register(RecipeTips)
