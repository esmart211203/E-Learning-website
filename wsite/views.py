from django.views import View
from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from .models import Category, Answer, Question, Subject, Class, SubImages, Lesson, Profile, Scholarship
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages 
# Create your views here.
def index(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    categories = Category.objects.all()
    high_score_users = User.objects.order_by('-profile__score')[:10]
    questions = Question.objects.order_by('-created_at')[:10]
    context = {
        "classes": classes,
        "subjects": subjects,
        "categories": categories,
        "questions": questions,
        "high_score_users": high_score_users,
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
class RegisterView(View):
    def get(self, request):
        return render(request, "auth/signup.html")
    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Tên người dùng hoặc email đã tồn tại.")
            return redirect('auth.register')
        user = User.objects.create_user(username=username, email=email, password=password)
        #create profile
        image = request.FILES.get('image')
        profile = Profile.objects.create(user=user, avatar=image)
        login(request, user)
        return redirect('index')
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
        profile = Profile.objects.get(user=user)
        profile.score += 5
        profile.save()
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

def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect("index")
@login_required(login_url='login')
def create_answer(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
        answer_content = request.POST.get('content')
        if not answer_content:
            return JsonResponse({'error': 'Answer content cannot be empty'}, status=400)
        user = request.user
        answer = Answer.objects.create(content=answer_content, question=question, user=user)
        profile = Profile.objects.get(user=user)
        profile.score += 10
        profile.save()
        files = request.FILES.getlist('sub_images')
        for file in files:
            sub_image = SubImages.objects.create(answer=answer,image=file) 
        return JsonResponse({'message': 'Answer created successfully', 'question_id': question_id}, status=201)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=400)

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

def lesson_detail(request, lesson_id):
    lesson = Lesson.lesson_detail(lesson_id=lesson_id)
    return render(request, 'lesson_detail.html', {'lesson': lesson})


### USER
def management_user(request):
    users = User.objects.all
    return render(request, 'admin/user/index.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
    return redirect('user.management')

### hoc bong
def management_scholarship(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'admin/scholarship/index.html', {'scholarships': scholarships})

class CreateCholarshipView(View):
    def get(self, request):
        return render(request, 'admin/scholarship/create.html')
    def post(self, request):
        title = request.POST.get('title')
        number_of_slots = request.POST.get('number_of_slots')
        scholarship_value = request.POST.get('scholarship_value')
        condition = request.POST.get('condition')
        form = request.POST.get('form')
        image = request.FILES.get('image')
        scholarship = Scholarship.objects.create(
            title=title,
            number_of_slots=number_of_slots,
            scholarship_value=scholarship_value,
            condition=condition,
            form=form,
            image=image,
        )
        return redirect('scholarship.management')

class EditCholarshipView(View):
    def get(self, request, scholarship_id):
        scholarship = get_object_or_404(Scholarship, pk=scholarship_id)
        return render(request, 'admin/scholarship/edit.html', {'scholarship': scholarship})
    def post(self, request, scholarship_id):
        title = request.POST.get('title')
        number_of_slots = request.POST.get('number_of_slots')
        scholarship_value = request.POST.get('scholarship_value')
        condition = request.POST.get('condition')
        form = request.POST.get('form')
        image = request.FILES.get('image')

        scholarship = get_object_or_404(Scholarship, pk=scholarship_id)

        scholarship.title = title
        scholarship.number_of_slots = number_of_slots
        scholarship.scholarship_value = scholarship_value
        scholarship.condition = condition
        scholarship.form = form
        if image:scholarship.image = image

        scholarship.save()
        return redirect('scholarship.management')

    
def delete_scholarship(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, pk=scholarship_id)
    if request.method == 'POST':
        scholarship.delete()
    return redirect('scholarship.management')


def scholarship_view(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarship.html', {'scholarships':scholarships})

def scholarship_detail(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, pk=scholarship_id)
    return render(request, 'scholarship_detail.html',{'scholarship': scholarship})

def chatbox(request):
    return render(request, 'chatbox.html')



def bot_response(request):
    if request.method == 'POST':
        question = request.POST.get('question', 'no content').lower()
        print("Câu hỏi:", question)
        if question == 'hi':
            response_data = {'response': 'Xin chào!'}
            print(response_data)
        elif question == 'bai':
            response_data = {'response': 'Tạm biệt!'}
            print(response_data)
        elif question in 'con khùng':
            response_data = {'response': 'là là là là là là là là =))))'}
        elif question in 'là ai':
            response_data = {'response': 'là ai còn lâu mới nói =))))'}
        else:
            response_data = {'response': 'Xin lỗi, tôi không thể hiểu câu hỏi của bạn.'}
            print(response_data)

        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'error': 'Yêu cầu không hợp lệ.'}, status=400)
