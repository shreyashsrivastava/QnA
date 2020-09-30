from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
	moderator = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.CharField(max_length=1000)
	def __str__(self):
		return self.question

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=5000)
    def __str__(self):
    	return self.answer