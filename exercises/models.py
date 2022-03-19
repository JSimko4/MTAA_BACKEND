from django.db import models
from users.models import User


class Exercise(models.Model):
    class Meta:
        db_table = "exercises"
    user = models.ForeignKey(User, related_name='exercises', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    body_parts = models.ManyToManyField("BodyPart")


class BodyPart(models.Model):
    class Meta:
        db_table = "body_parts"
    name = models.CharField(max_length=255)


