from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    ## admin
    path('site-admin', views.admin, name='admin.index'),
    ## lesson
    path('lesson/management', views.management_lesson, name='lesson.management'),
    path('lesson/create', views.CreateLessonView.as_view(), name='lesson.create'),
    path('lesson/<int:lesson_id>', views.delete_lesson, name='lesson.delete'),
    path('lesson/edit/<int:lesson_id>', views.EditLessonView.as_view(), name='lesson.edit'),
    ## auth 
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    ## questions
    path('question', views.create_question, name='question.create'),
    path('question/<int:question_id>', views.detail_question, name='question.detail'),
    path('answer/<int:question_id>', views.create_answer, name='answer.create'),
    ### front end
    path('quiz', views.view_quiz, name='quiz.index'),
    path('lesson', views.view_lesson, name='lesson.index'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)