import uuid

from django.db import models
from django.utils.timezone import now


class Reader(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50, blank=True)


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=20)


class Book(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=100, blank=True)
    readers = models.ManyToManyField(Reader, through='Rental')
    category = models.ForeignKey(Category)


class Rental(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    rent_date = models.DateTimeField(default=now)
    return_date = models.DateTimeField(null=True, blank=True)
    reader = models.ForeignKey(Reader)
    book = models.ForeignKey(Book)
    rating = models.DecimalField(default=5.0, max_digits=2, decimal_places=1)
