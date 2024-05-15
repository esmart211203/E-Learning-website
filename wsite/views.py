from django.views import View
from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from .models import Category, Answer, Question, Subject, Class, SubImages
from django.http import JsonResponse
# Create your views here.
def index(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    categories = Category.objects.all()
    questions = Question.objects.order_by('-created_at')
    context = {
        "classes": classes,
        "subjects": subjects,
        "categories": categories,
        "questions": questions,
    }
    return render(request, 'index.html', context)

def sidebar(request):
    subjects = Subject.objects.all()
    return render(request, "sidebar.html", {'subjects': subjects})
## AUTH ##
class LoginView(View):
    def get(self, request):
        return render(request, "auth/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            context = {
                "error_message": "Đăng nhập không thành công. Vui lòng kiểm tra lại tên người dùng và mật khẩu."
            }
            return render(request, "auth/login.html", context)
        login(request, user)
        return redirect("index")

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect("index")

## QUESTION MARK
@login_required(login_url='login')
def createQuestion(request):
    user = request.user 
    if request.method == "POST":
        class_field_id = request.POST.get("category")
        class_field = Class.objects.get(id=class_field_id)
        subject_id = request.POST.get("subject")
        subject = Subject.objects.get(id=subject_id)
        content = request.POST.get("content")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        files = request.FILES.getlist('sub_images') 
        question = Question.objects.create(user=user, class_field=class_field, subject=subject, content=content, category=category)
        for file in files:
            sub_image = SubImages.objects.create(question=question,image=file)
    return redirect("index")

def detailQuestion(request, question_id):
    subjects = Subject.objects.all()
    question = Question.objects.get(id=question_id)
    answers = Answer.objects.filter(question_id=question_id)
    question_images = SubImages.objects.filter(question_id = question.id)
    context = {
        "subjects": subjects,
        "question_id": question_id,
        "question": question,
        "answers": answers,
        "sub_images": question_images,
    }
    return render(request, 'detail_question.html', context)

@login_required(login_url='login')
def createAnswer(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
        answer_content = request.POST.get('content')
        if not answer_content:
            return JsonResponse({'error': 'Answer content cannot be empty'}, status=400)
        answer = Answer.objects.create(content=answer_content, question=question, user=request.user)
        files = request.FILES.getlist('sub_images')
        for file in files:
            sub_image = SubImages.objects.create(answer=answer,image=file) 
        return JsonResponse({'message': 'Answer created successfully', 'question_id': question_id}, status=201)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=400)
    


def viewQuiz(request):
    return render(request, 'quiz.html')