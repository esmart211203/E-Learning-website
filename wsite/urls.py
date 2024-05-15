from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    ## auth 
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logoutUser, name='logout'),
    ## questions
    path('question', views.createQuestion, name='question.create'),
    path('question/<int:question_id>', views.detailQuestion, name='question.detail'),
    path('answer/<int:question_id>', views.createAnswer, name='answer.create'),

    path('quiz', views.viewQuiz, name='quiz.index'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)