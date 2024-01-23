from django.db import models
from profiles.models import UserProfile
# Create your models here.


class FlowerCategories(models.Model):
    category_name = models.CharField(max_length=100)
    category_description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.category_name


class Flower(models.Model):
    seller = models.ForeignKey(
        UserProfile, related_name='seller_flower', on_delete=models.CASCADE)
    category = models.ForeignKey(
        FlowerCategories, related_name='category_flower', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.PositiveIntegerField(default=0)
    image_url = models.URLField()

    def __str__(self):
        return self.title


class OrderHistory(models.Model):
    user = models.ForeignKey(
        UserProfile, related_name='order_user', on_delete=models.CASCADE)
    flower = models.ForeignKey(
        Flower, related_name='order_flower', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default='Pending')
    total_price = models.IntegerField(null=True, blank=True)
    all_quantity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.user.username} {self.flower.title}'
