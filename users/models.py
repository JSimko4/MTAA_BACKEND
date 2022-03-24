from django.db import models


class User(models.Model):
    class Meta:
        db_table = "users"
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
