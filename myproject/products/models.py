from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    stock = models.PositiveIntegerField()
    image_url = models.URLField(max_length=500)
    ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
