from django.db import models

# Create your models here.


class Course(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):

        return self.name
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    admission_date = models.DateField(auto_now_add=True)
    course = models.ForeignKey(Course,on_delete=models.PROTECT,related_name="students")
    """courses = models.ManyToManyField(
        Course,
        related_name="students"
    )"""
    photo = models.ImageField(upload_to="students/",blank=True,null=True)
    def __str__(self):
        return self.name
    
