from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'questions/answer', views.AnswerViewSet)

urlpatterns = [
	path('', include(router.urls)),

    path('auth/login/', views.user_login, name='login'),
    path('auth/logout/', views.user_logout, name='logout'),
    path('question/create/', views.post_question, name='post_question'),
    path('answer/create/', views.post_answer, name='post_answer'),
]