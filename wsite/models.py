from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Class(models.Model):
    class_number = models.PositiveIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Lớp {self.class_number}"
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE, default='')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default='')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def getClass(self):
        return f"{self.class_field}"
    def __str__(self):
        return self.content

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content 
    def get_images(self):
        return SubImages.objects.filter(answer=self)
class SubImages(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.image.url