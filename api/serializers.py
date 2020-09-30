from rest_framework import serializers
from .models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = [ 'moderator', 'question']

class AnswerSerializer(serializers.ModelSerializer):
	question = QuestionSerializer(read_only=True)
	class Meta:
		many = True
		model = Answer
		fields = '__all__'