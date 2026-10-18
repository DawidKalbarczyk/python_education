from django.db import models

class PriorityChoices(models.IntegerChoices):
    LOW = 1, 'Low'
    MEDIUM = 2, 'Medium'
    HIGH = 3, 'High'

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    done = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    priority = models.IntegerField(PriorityChoices.choices, default=PriorityChoices.MEDIUM)

    def __str__(self):
        return f"{self.id} - {self.title}"