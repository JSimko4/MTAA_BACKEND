from django.db import models


class Users(models.Model):
    class Meta:
        db_table = "users"
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
