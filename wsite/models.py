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
    def is_author(self, user):
            return self.user == user
    def getClass(self):
        return f"{self.class_field}"
    def __str__(self):
        return self.content
    def get_count_react_question_like(self):
            return React.objects.filter(question=self.pk, status='like').count()
    def get_count_react_question_dislike(self):
            return React.objects.filter(question=self.pk, status='dislike').count()
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
    image = models.ImageField(max_length=255, upload_to='subimages')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.image.url

class Lesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,blank=True)
    content = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(max_length=255, blank=True, null=True)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    def lesson_detail(lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        lesson.view_count = lesson.view_count + 1
        return lesson
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(max_length=255, upload_to='profile', blank=True, null=True)
    score = models.IntegerField(default=0)

class Scholarship(models.Model):
    title = models.CharField(max_length=255)
    number_of_slots = models.IntegerField()
    scholarship_value = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    form = models.CharField(max_length=255)
    image = models.ImageField(max_length=255, upload_to='scholarship')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class React(models.Model):
    STATUS_CHOICES = (
        ("like", "Thích"),
        ("dislike", "Không thích"),
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True,null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="like")
    created_at = models.DateTimeField(auto_now_add=True)



    def get_count_react_answer(self):
        return React.objects.filter(answer=self.answer).count()