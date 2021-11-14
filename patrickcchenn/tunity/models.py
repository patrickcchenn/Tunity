from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.
class User(AbstractUser):
    pass


class company(models.Model):
    year = models.DateField()
    body = models.TextField(max_length=40)
    country = models.CharField(max_length=40)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="is_company"
    )

class CV(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="CV"
    )
    file_field = models.FileField(upload_to='uploads/%Y/%m/%d/')

class vacancy(models.Model):
    position = models.CharField(max_length=40)
    starting_hour = models.CharField(max_length=40, null=True)
    ending_hour = models.CharField(max_length=40, null=True)
    starting_day = models.CharField(max_length=40, null=True)
    ending_day = models.CharField(max_length=40, null=True)
    description = models.CharField(max_length=40, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vacancies")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.position}-{self.user}"


class applied(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applied")
    list = models.ManyToManyField(vacancy, related_name="applicants", blank=True)


class condition(models.Model):
    accepted = models.BooleanField()
    job = models.ForeignKey(vacancy, on_delete=models.CASCADE, related_name="condition")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accepted")
