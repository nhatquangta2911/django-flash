from django.db import models

# Create your models here.


class Result(models.Model):
    QUESTION_PERIOD_CHOICES = (
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening')
    )
    QUESTION_TYPE_CHOICES = (
        ('YesNo', 'YesNo'),
        ('SingleChoice', 'SingleChoice'),
        ('MultiChoice', 'MultiChoice'),
        ('DropdownList', 'DropdownList'),
    )
    QUESTION_CONTENT_TYPE_CHOICES = (
        ('Food', 'Food'),
        ('Exercise', 'Exercise'),
        ('WaterConsumption', 'WaterConsumption')
    )
    JOB_CHOICES = (
        ('Engineer', 'Engineer'),
        ('Student', 'Student'),
        ('Driver', 'Driver'),
        ('TourGuide', 'TourGuide'),
    )

    questionperiod = models.CharField(
        max_length=20, choices=QUESTION_PERIOD_CHOICES)
    questiontype = models.CharField(
        max_length=30, choices=QUESTION_TYPE_CHOICES)
    questioncontenttype = models.CharField(
        max_length=30, choices=QUESTION_CONTENT_TYPE_CHOICES)
    job = models.CharField(max_length=20, choices=JOB_CHOICES)

    def __str__(self):
        return self.questiontype, self.questionperiod, self.questioncontenttype, self.job
