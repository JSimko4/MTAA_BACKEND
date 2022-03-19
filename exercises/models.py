from django.db import models


class Exercise(models.Model):
    class Meta:
        db_table = "exercises"
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)


class ExerciseBodyPart(models.Model):
    class Meta:
        db_table = "exercise_body_parts"
    exercise_id = models.IntegerField()
    body_part_id = models.IntegerField()


class BodyPart(models.Model):
    class Meta:
        db_table = "body_parts"
    name = models.CharField(max_length=255)
