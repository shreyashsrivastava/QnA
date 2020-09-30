from .models import Question, Answer
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

@csrf_exempt
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['email']
            password = request.POST['password']
            user_model = get_user_model()
            print(user_model)
            print(password)
        try:
            user = user_model.objects.get(username=username)
            print(user)
            if user.check_password(password):
                login(request, user)
                return JsonResponse({"message": "Login successfull.",
                                     "body": {
                                                "user":{
                                                    "email": user.username,
                                                    "status": "Activated",
                                                    },
                                                    "userID": user.id,
                                                    "role": "Moderater" if user.is_staff else "User",
                                            },
                                    "status": 200
                                    })
            else:
                return JsonResponse({'error':"Invalid password"})
        except user_model.DoesNotExist:
            return JsonResponse({"message": "You do not have an account please signup to continue.",
                                 "error": "error",
                                 "status": 401
                                })
        else:
            return JsonResponse({'error':"Not a POST request"})
    else:
        return JsonResponse({'error':"You're already logged in"})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'success':'Logged Out Successfully'})
    else:
        return JsonResponse({'message':'Please login first'})

@csrf_exempt
def post_question(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            question = request.POST['question']
            Question.objects.create(moderator=request.user, question=question)
            return JsonResponse({
                                    "message": "question created.",
                                    "body": question,
                                    "status": 200
                                })
        else:
            return JsonResponse({
                                    "message": "Only Moderator can post questions",
                                    "error": "error",
                                    "status": 401
                                })
    else:
        return JsonResponse({'error':'You should login first'})


@csrf_exempt
def post_answer(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            answer = request.POST['answer']
            questionID = request.POST['questionID']
            print(questionID)
            question = get_object_or_404(Question, pk=questionID)
            Answer.objects.create(question=question, answer=answer)
            return JsonResponse({
                                    "message": "answer created.",
                                    "body": answer,
                                    "status": 200
                                })
        else:
            return JsonResponse({'message':'You are not allowed', 'error':'401'})
    else:
        return JsonResponse({'error':'You Should Login First'})


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer



