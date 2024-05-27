from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime

# Create your models here.
class Tags(models.Model):
    tag_text = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.tag_text

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("data published")
    tags = models.ManyToManyField(Tags)

    @admin.display(
            boolean=True,
            ordering="pub_date",
            description="Published recently?",
            )

    def was_published_recently(self):
        return self.pub_date >= timezone.localtime(timezone.now()) - datetime.timedelta(days=1)
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question_text = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default= 0)

    def __str__(self):
        return self.choice_text
    
