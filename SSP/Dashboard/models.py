from django.db import models
from django.contrib.auth.models import User



# Create your models here.
# vai@123
# vaibhav

# models to create table
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE) #when username is deleted then notes of the user also deleted
    title = models.CharField(max_length = 20)
    desc = models.TextField()

    # to display the notes on admin site
    def __str__(self):
        return self.title


# to change the plural name of notes on admin site
    class Meta:
        verbose_name = "Notes"
        verbose_name_plural = "Notes"

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    Subject = models.CharField(max_length=50)
    Title = models.CharField(max_length=50)
    Description = models.TextField()
    Due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.Subject



class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title

 