from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import os
# Create your models here.

QUES_TYPE = (
    (1, ("C")),
    (2, ("CI")),
    (3, ("CIP"))
)

BOARD = (
    (1, ("CBSE")),
    (2, ("ICSE")),
    (3, ("IQ"))
)

    
class BoardClassChapter(models.Model):
    board = models.IntegerField(choices=BOARD)
    class_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    chapter_num = models.IntegerField()
    chapter = models.CharField(max_length=200)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

class ChapterTopic(models.Model):
    chapter = models.ForeignKey(BoardClassChapter,on_delete=models.CASCADE,related_name="topic_chapter_info")
    topic = models.CharField(max_length=300)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

class ChapterPrerequisite(models.Model):
    chapter = models.ForeignKey(BoardClassChapter,on_delete=models.CASCADE,related_name="prerequisite_chapter_info")
    prerequisite = models.ForeignKey(ChapterTopic,on_delete=models.CASCADE,related_name="prerequisite_topic_info")
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

from uuid import uuid4
def get_unique_full_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(str(instance.pk)+uuid4().hex,ext)
    # return the whole path to the file
    return os.path.join('images/', filename)

class AdaptiveQuestion(models.Model):
    #user = models.ForeignKey(User,on_delete=models.PROTECT)
    chapter_topic = models.ForeignKey(ChapterTopic,on_delete=models.PROTECT,related_name="question_chapter_info")
    question  = models.TextField()
    answer = models.CharField(max_length=10)
    #it is question prerequisite not chapter
    image = models.ImageField(upload_to=get_unique_full_path, max_length=200, blank=True, null=True)
    ques_type = models.IntegerField(choices=QUES_TYPE)
    level = models.IntegerField(validators=[MinValueValidator(0)])
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

class AdaptiveQuestionOptions(models.Model):
    question = models.OneToOneField(AdaptiveQuestion,on_delete=models.CASCADE)
    option_a  = models.TextField()
    option_b  = models.TextField()
    option_c  = models.TextField(blank=True,null=True)
    option_d  = models.TextField(blank=True,null=True)

class AdaptiveQuestionTopics(models.Model):
    question = models.ForeignKey(AdaptiveQuestion,on_delete=models.CASCADE,related_name="topic_question_info")
    topic =  models.ForeignKey(ChapterTopic,on_delete=models.PROTECT)

class AdaptiveQuestionPrerequisite(models.Model):
    question = models.ForeignKey(AdaptiveQuestion,on_delete=models.CASCADE)
    prerequisite =  models.ForeignKey(ChapterTopic,on_delete=models.PROTECT)