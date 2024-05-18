from django.views import View
from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from .models import Category, Answer, Question, Subject, Class, SubImages, Lesson
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
def logout_user(request):
    logout(request)
    return redirect("index")

## QUESTION MARK
@login_required(login_url='login')
def create_question(request):
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

def detail_question(request, question_id):
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
def create_answer(request, question_id):
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
    


def view_quiz(request):
    return render(request, 'quiz.html')

def view_lesson(request):
    lessons = Lesson.objects.all()
    first_lesson = lessons.order_by('-created_at').first()
    lesson_featured = Lesson.objects.order_by('-view_count')[:2]
    context = {
        "first_lesson": first_lesson,
        "lessons": lessons,
        "lesson_featured": lesson_featured,
    }
    return render(request, 'lesson.html', context)
### ADMIN ###
def admin(request):
    return render(request, 'admin/index.html')
## COURSE ##
def management_lesson(request):
    lesson = Lesson.objects.all
    return render(request, 'admin/lesson/index.html', {'lesson': lesson})
class CreateLessonView(View):
    def get(self, request):
        classes = Class.objects.all()
        subjects = Subject.objects.all()
        
        context = {
            "classes": classes,
            "subjects": subjects,
        }
        return render(request, 'admin/lesson/create.html', context)
    def post(self, request):
        user = request.user
        subject_id = request.POST.get('subject')
        subject = Subject.objects.get(id=subject_id)
        class_field_id = request.POST.get('class_field')
        class_field = Class.objects.get(id=class_field_id)
        title = request.POST.get('title')
        content = request.POST.get('content')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        if not all([subject, class_field, title, content]):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        lesson = Lesson.objects.create(
                        user=user, 
                        subject=subject, 
                        class_field=class_field, 
                        title=title, 
                        content=content,
                        image=image,
                        description=description,
                    )
        return redirect('lesson.management')
class EditLessonView(View):
    def get(self, request, lesson_id):
        classes = Class.objects.all()
        subjects = Subject.objects.all()
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        context = {
            "classes": classes,
            "subjects": subjects,
            "lesson": lesson,
        }
        return render(request, 'admin/lesson/edit.html', context)
    def post(self, request, lesson_id):
        subject_id = request.POST.get('subject')
        subject = Subject.objects.get(id=subject_id)
        class_field_id = request.POST.get('class_field')
        class_field = Class.objects.get(id=class_field_id)
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        lesson.subject = subject
        lesson.class_field = class_field
        lesson.title = title
        lesson.content = content
        lesson.image = image
        lesson.description = description

        lesson.save()
        return redirect('lesson.management')
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.method == 'POST':
        lesson.delete()
    return redirect('lesson.management')