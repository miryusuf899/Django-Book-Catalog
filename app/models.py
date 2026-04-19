from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid

class UserModel(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=False, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)    
    password = models.CharField(max_length=225)

    is_active = models.BooleanField(default=False)
    email_token = models.UUIDField(default=uuid.uuid4, editable=False)
    reset_token = models.UUIDField(null=True, blank=True) 

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.username
    

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class Author(models.Model):
    full_name = models.CharField(max_length=20)
    bio = models.TextField(max_length=100)

    def __str__(self):
        return self.full_name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover_image = models.ImageField(upload_to='books/')
    created_at = models.TimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.book.title} by {self.user.username}"