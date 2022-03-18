from django.db import models


class Exercises(models.Model):
    class Meta:
        db_table = "exercises"
    user_id = int
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)


class ExerciseBodyParts(models.Model):
    class Meta:
        db_table = "exercise_body_parts"
    exercise_id = int
    body_part_id = int


class BodyParts(models.Model):
    class Meta:
        db_table = "body_parts"
    name = models.CharField(max_length=255)
