from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
# Create your models here.
class Student(models.Model):
    registration_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField()
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="student_photos/", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class DailyQuota(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_quotas")
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quota_date = models.DateField(default=datetime.datetime.now().date())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name


EXPENSE_CHOICES = (
    ("lunch", "Lunch"),
    ("breakfast", "Breakfast"),
    ("supper", "Supper"),
)

class StudentExpediture(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_expediture")
    daily_quota = models.ForeignKey(DailyQuota, on_delete=models.CASCADE, related_name="quota_expeditures")
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expense = models.CharField(max_length=255, choices=EXPENSE_CHOICES)
    expenditure_date = models.DateField(default=datetime.datetime.now().date())
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.student.name + " " + self.expense


class MealCard(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=255)
    #allocation_today = models.DecimalField(max_digits=10, decimal_places=2)
    #amount_spent_today = models.DecimalField(max_digits=10, decimal_places=2)
    #balance_today = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.student.name + " " + self.card_number
