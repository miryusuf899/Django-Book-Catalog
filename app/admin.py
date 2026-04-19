from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import UserModel, Category, Author, Book, Review


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)


admin.site.unregister(User)
admin.site.unregister(Group)