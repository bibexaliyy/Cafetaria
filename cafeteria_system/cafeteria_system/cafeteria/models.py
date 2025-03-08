from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fingerprint_id = models.CharField(max_length=255, unique=True)
    school_category = models.CharField(max_length=100)
    meal_balance = models.IntegerField(default=30)  

    def __str__(self):
        return self.user.username


class Meal(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MealTransaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class MealTicket(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE) 
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)  
    date = models.DateField(auto_now_add=True)  
    validity_days = models.IntegerField(default=1)  

    def __str__(self):
        return f"{self.student.username} - {self.meal.name} ({self.date})"  

class AuditLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_meals_collected = models.IntegerField(default=0)
    month = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student.user.username} - {self.month}"


class AdminRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[
        ("caterer", "Caterer Supervisor"),
        ("student_affairs", "Student Affairs"),
        ("audit", "Audit & PMIC"),
    ])

    def __str__(self):
        return f"{self.user.username} - {self.role}"
